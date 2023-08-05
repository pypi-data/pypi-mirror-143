# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=invalid-name, unused-argument
"""The integration of the Arm(R) Ethos(TM)-U NPU TIR compiler."""
import tvm
from tvm import relay
from tvm.relay.expr_functor import ExprMutator
from tvm.driver.build_module import schedule_to_module

from .passes import ReplaceOperators, RemoveZeroStores, EncodeConstants
from .scheduler import schedule


def lower_ethosu(sch, args, const_dict, name="main"):
    """Lower a schedule to TIR for the Arm(R) Ethos(TM)-U NPU target.

    The resulting TIR module will contain a single function
    that consists of a sequence of tir.call_extern to NPU
    operations.

    Parameters
    ----------
    sch : tvm.te.Schedule
        The schedule to be lowered.
    args : Union[list of tvm.te.Tensor, TEGraph]
        The input/output tensors.
    const_dict : dict of int to numpy.ndarray
        The constant dictionary.
    name : str, optional
        The name of the lowered primitive function.

    Returns
    -------
    mod : tvm.IRModule
        The lowered TIR module.
    const_dict : dict of int to numpy.ndarray
        The modified constant dictionary.

    """
    if not isinstance(args, list):
        args = list(args.inputs) + list(args.outputs)
    # config setup
    curr_pass_ctx = tvm.ir.transform.PassContext.current()
    curr_cfg = dict()
    for key, value in curr_pass_ctx.config.items():
        curr_cfg[key] = value
    tir_compiler_cfg = {
        "tir.LoopPartition": {
            "partition_const_loop": True,
            "no_unroll_loop_with_extent_one": True,
        },
        "tir.UnrollLoop": {"auto_max_depth": -1},
        "tir.noalias": True,
        "tir.debug_keep_trivial_loop": True,
    }
    # Merge two configs
    curr_cfg = {**curr_cfg, **tir_compiler_cfg}

    sch = sch.normalize()

    with tvm.transform.PassContext(config=curr_cfg):
        mod = schedule_to_module(sch, args, name)

        mod = tvm.tir.transform.Simplify()(mod)
        mod = tvm.tir.transform.StorageFlatten(64)(mod)
        mod = tvm.tir.transform.UnrollLoop()(mod)
        mod = tvm.tir.transform.Simplify()(mod)
        mod = tvm.tir.transform.LoopPartition()(mod)
        mod = RemoveZeroStores()(mod)
        mod = tvm.tir.transform.Simplify()(mod)
        mod = tvm.tir.transform.RemoveNoOp()(mod)
        mod = ReplaceOperators()(mod)
        mod = tvm.tir.transform.RemoveNoOp()(mod)
        mod, const_dict = EncodeConstants(const_dict)(mod)
        mod = tvm.tir.transform.StorageRewrite()(mod)
        mod = tvm.tir.transform.RemoveNoOp()(mod)
    return mod, const_dict


def lower_to_te(prim_func):
    """Lower a Relay primitive function to a Tensor Expression in an unscheduled CachedFunc.

    Parameters
    ----------
    prim_func : tvm.relay.Function
        The Relay function to lower.

    Returns
    -------
    out : CachedFunc
        The lowered Tensor Expression as part of a CachedFunc.

    """
    f = tvm._ffi.get_global_func("relay.backend.LowerToTE")
    return f(prim_func)


class ExtractConstants(ExprMutator):
    """The actual mutator pass to extract the constants from a function and replace them with
    Vars so the function can be lowered to a TE graph. Additionally returns all the values of
    the constants extracted."""

    def __init__(self):
        super().__init__()
        self.constants = []

    def visit_constant(self, const):
        if isinstance(const.checked_type, relay.ty.TensorType):
            if const.checked_type.concrete_shape != ():
                self.constants.append(const.data.asnumpy())
                name = "p" + str(len(self.constants))
                return relay.var(type_annotation=const.checked_type, name_hint=name)

        return const

    def visit_function(self, fn):
        new_body = self.visit(fn.body)
        new_params = list(relay.analysis.free_vars(new_body))
        return relay.Function(new_params, new_body)

    def extract_constants(self, func):
        new_func = self.visit(func)
        return new_func, self.constants


def extract_constants(func):
    """Extract the constants from a function and replace them with
    Vars so the function can be lowered to a TE graph. Additionally
    returns all the values of the constants extracted.

    Parameters
    ----------
    func : tvm.relay.Function
        The Relay function from which to extract constants.

    Returns
    -------
    new_func : tvm.relay.Function
        The Relay function with constants replaced by vars.
    const_dict : dict of int to numpy.ndarray
        A dict of the extracted constants keyed by their param index.

    """
    const_dict = {}
    params = len(func.params)
    new_func, consts = ExtractConstants().extract_constants(func)
    for i, const in enumerate(consts):
        const_dict[params + i] = const

    new_func = tvm.relay.transform.InferType()(tvm.IRModule.from_expr(new_func))["main"]
    return new_func, const_dict


def lower_to_tir(func, cascader=None):
    """Lower a Relay function to TIR for the Arm(R) Ethos(TM)-U NPU target.

    The Relay function should only contain operations supported
    by the NPU.

    Parameters
    ----------
    func : tvm.relay.Function
        The Relay function to lower.
    cascader : Callable
        An optional cascading function,

    Returns
    -------
    mod : tvm.IRModule
        The lowered TIR module.
    consts : dict of int to numpy.ndarray
        A dict of the extracted constants keyed by their param index.

    """
    func, consts = extract_constants(func)
    mod = tvm.IRModule.from_expr(func)
    func = relay.transform.InferType()(mod)["main"]
    cached_func = lower_to_te(func)
    s = schedule(cached_func, consts, cascader)
    mod, consts = lower_ethosu(s, cached_func, consts)
    return mod, consts
