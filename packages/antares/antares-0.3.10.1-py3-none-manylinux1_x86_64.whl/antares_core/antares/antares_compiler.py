# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import sys, time, subprocess, os
import random
import hashlib
import traceback
import math
import re
import json
import importlib
import signal
import collections
import threading

from antares.common import *
from graph_evaluator import client as eval_client

compiler_path = os.path.dirname(os.path.abspath(__file__))
antares_driver_path = os.environ['ANTARES_DRIVER_PATH']

AntaresGlobal.cleanup_funcs = []
use_progress = int(os.environ.get('PROGRESS', 0)) == 1

if use_progress:
  def print_none(*args, **kwargs):
    pass
  progress_print, print = print, print_none

save_path = None
if len(sys.argv) > 1:
  if sys.argv[1] == 'save':
    save_path = sys.argv[2]
    if not save_path.startswith('/'):
      work_dir = os.environ['WORKDIR']
      if not work_dir.endswith('/'):
        work_dir += '/'
      save_path = work_dir + save_path
  elif sys.argv[1] == 'torch-setup':
    sys.argv = sys.argv[:1] + sys.argv[2:]
    from frameworks.pytorch import setup
    exit(0)
  elif sys.argv[1] == 'tf-setup':
    sys.argv = sys.argv[:1] + sys.argv[2:]
    from frameworks.tensorflow import setup
    exit(0)
  elif sys.argv[1] == 'exec':
    os.chdir(os.environ.get('WORKDIR', '.'))
    os.execl(sys.executable, sys.executable, *sys.argv[2:])
  else:
    raise Exception('Unsupported command arguments: %s' % ' '.join(sys.argv[1:]))

def save_to_path_if_necessary(saved_code):
  if save_path is None:
    return
  with open(save_path, 'w') as fp:
    fp.write(saved_code)

def cleanup_on_exit(signum, frame):
  for func in AntaresGlobal.cleanup_funcs:
    try:
      func()
    except:
      pass
  exit(0 if signum == -1 else 1)

signal.signal(signal.SIGINT, cleanup_on_exit)

verbose = int(os.environ.get('VERBOSE', '1'))

try:
  backend_config = importlib.import_module('backends.%s.config' % backend)
  backend_root = os.path.dirname(backend_config.__file__)
except ModuleNotFoundError:
  raise Exception('>> Platform config for backend %s not found' % backend)
except:
  traceback.print_exc()
  exit(1)


def compute_gflops(flop, t):
  try:
    return flop / (t * 1e3) / 1e6
  except:
    return 0.0

def codehub_db(compute_key, source_code=None, erase=False):
  compute_key = compute_key.split('##')[0].strip()
  digest = hashlib.sha256(compute_key.encode()).hexdigest()
  os.system('mkdir -p %s/codehub' % antares_driver_path)
  code_path = '%s/codehub/%s.%s' % (antares_driver_path, digest, backend)
  if erase:
    try:
      os.remove(code_path)
    except:
      pass
    return None
  if not source_code:
    if os.path.exists(code_path):
      print('  >> Codehub Key = %s.%s' % (digest, backend))
      with open(code_path, 'r') as fp:
        code = fp.read()
      return code
    else:
      return None
  else:
    with open(code_path, 'w') as fp:
      fp.write(source_code)
    return code_path

def get_target_source(best_config, dir_sid=None):
  # Note: Not thread safe due to multiple invokes of target codegen

  global_arg_props = AntaresGlobal.global_arg_props
  def get_kernel_metadata(config):
    inp_args, outp_args = [], []

    for buf in global_arg_props['_in']:
      if buf['name'].startswith('_'):
        # Just for Auto Shard
        assert(buf['dtype'] == 'int32' and buf['shape'] == [1])
        continue
      inp_args.append('%s:%s%s' % (buf['name'], buf['dtype'], buf['shape']))
    for buf in global_arg_props['_out']:
      outp_args.append('%s:%s%s' % (buf['name'], buf['dtype'], buf['shape']))

    device_code = os.environ.get('DEVICE_NAME', '')
    device_code = device_code if device_code else 'default'
    header_meta = '// GLOBALS: ' + ', '.join(inp_args) + ' -> ' + ', '.join(outp_args) + '\n// BACKEND: %s (%s)\n' % (backend, device_code)
    properties = "// CONFIG: %s\n// COMPUTE_V1: %s\n" % (config.strip() if isinstance(config, str) else '', os.environ['COMPUTE_V1'])
    return header_meta + properties

  def slices_to_code(kernel_slices):
    def tensor_display(encoded_name, prop):
      return f'{encoded_name}:{prop["dtype"]}{str(prop["shape"])}'

    kernel_slices.sort()
    code = ['']
    for i, (kernel_id, kernel_name, args, body) in enumerate(kernel_slices):
      num_outputs = len(global_arg_props['_out']) if i + 1 == len(kernel_slices) else 1
      display_inputs = ', '.join([tensor_display(x, prop) for _, x, prop in args[:-num_outputs]])
      display_outputs = ', '.join([tensor_display(x, prop) for _, x, prop in args[-num_outputs:]])
      kernel = backend_config.do_native_translation_v2((kernel_name, args[:-num_outputs], args[-num_outputs:], body), attrs=getattr(AntaresGlobal, 'attrs', None)).strip()
      code.append(f'// LOCAL: {kernel_name} -- {display_inputs} -> {display_outputs}\n\n{kernel}\n')

    del kernel_slices
    code = '\n// ---------------------------------------------------------------------------\n'.join(code)
    return code

  def pack_device_source(kernel_slices):
    device_source = slices_to_code(kernel_slices)
    device_source = '%s\n%s' % (get_kernel_metadata(best_config), device_source)
    kernel_path = local_get_dir_file('my_kernel.cc', dir_sid=dir_sid)
    with open(kernel_path, 'w') as fp:
      fp.write(device_source)
    return device_source, kernel_path

  json_config = json.loads(best_config)
  kernel_slices = backend_config.to_kernel_slices(AntaresGlobal.compute_graph, json_config if json_config is not None else {})
  return pack_device_source(kernel_slices)


def code_suffix(tpr=-1.0, step_prod=0, step_plan=-1):
  return '\n// Saved Perf = %.6e sec / run; Step Produced = %d; Planned Steps = %d;' % (tpr, step_prod, step_plan)

def evaluate_perf(kernel_path, dev_id, device_source, dir_sid=None, verbose=True, expected_timeout=None):
  if verbose:
    print("\n[EvalAgent] Evaluating Modules..\n")

  def handle_result(result):
    if verbose:
      print('\n[EvalAgent] Results =', json.dumps(result))
    if 'RESULT' in os.environ:
      if abs(float(os.environ['RESULT']) / result['K/0'] - 1.0) > 1e-6:
        result['TPR'] = None

    t = result.get('TPR', None)
    if 'K/0' in result and t is None:
      t = result['TPR'] = float('inf')
    if t is None:
      print("\n[Antares] Incorrect compute kernel from evaluator.")
    else:
      gflops = compute_gflops(AntaresGlobal.default_task.flop, t)
      if verbose:
        print("\n[Antares] Average time cost / run = %g sec, %g gflops." % (t, gflops))
      with open(local_get_dir_file('result.txt', dir_sid=dir_sid), 'w') as fp:
        fp.write(str(t) + '\n')
        for i in range(len(result)):
          key = 'K/%d' % i
          if key not in result:
            break
          fp.write(str(result[key]) + '\n')
    if os.environ.get('COMMIT', ''):
      kernel_path = codehub_db(os.environ['COMPUTE_V1'], source_code=device_source + code_suffix(tpr=t))
      print('  >> Update current code to codehub: %s' % kernel_path)

  def do_evaluate(expected_timeout):
    try:
      if expected_timeout is None:
        expected_timeout = os.environ.get('EXPECTED_TIMEOUT', 'inf')
      if expected_timeout in ('', 'inf', float('inf')):
        expected_timeout = ''
      else:
        expected_timeout = float(expected_timeout)
        expected_timeout = max(expected_timeout * 1.1, expected_timeout + 0.1)

      results = eval_client.eval(kernel_path=local_get_dir_file('my_kernel.cc', dir_sid=dir_sid),
                  expected_timeout=expected_timeout,
                  dev_id=dev_id, backend_root=backend_root
                )
      return results
    except SystemExit:
      return None
    except:
      if verbose:
        traceback.print_exc()
      return None

  try:
    results = do_evaluate(expected_timeout)
    if results is not None:
      handle_result(results)
  except:
    pass
  return results

def compute_mem_ratio(tpr):
  if math.isinf(tpr) or math.isinf(float(AntaresGlobal.attrs.device_props.mem_bandwith)) or AntaresGlobal.attrs.device_props.mem_bandwith <= 0:
    return -1

  global_arg_props = AntaresGlobal.global_arg_props
  access_bytes = 0
  for buf in global_arg_props['_in']:
    access_bytes += product(buf['shape']) * get_type_size(buf['dtype'])
  for buf in global_arg_props['_out']:
    access_bytes += product(buf['shape']) * get_type_size(buf['dtype'])

  access_bytes = int(access_bytes)
  if access_bytes <= 0:
    return -1
  ratio = math.ceil(access_bytes * 1e-7 / tpr / AntaresGlobal.attrs.device_props.mem_bandwith)
  return min(int(ratio), 100)

def run_config_entity(target_source, config_str, dir_sid, expected_timecost='inf', dev_id=0):
  config_str_short = config_str # if len(config_str) < 60 else config_str[:60] + '..'
  print("  >> [ ] Param_entity on sid = %s: config = '%s', dev_id = %d, upper_bound_tpr = %.6e s" % (dir_sid, config_str_short, dev_id, expected_timecost))
  try:
    assert target_source is not None, "Invalid target source detected in verification stage."
    device_source, kernel_path = target_source

    results = evaluate_perf(kernel_path, dev_id, device_source, dir_sid, verbose=False, expected_timeout=expected_timecost)
    assert results is not None and 'TPR' in results, "Invalid target output detected in evaluation stage."
    digest = ','.join(['%.6e' % float(results['K/%d' % i]) for i in range(len(results) - 1)])
    digest = f'\033[{91 + int(hashlib.sha256(digest.encode()).hexdigest(), 16) % 6}m{digest}\033[0m'
    result = float(results['TPR'])
  except:
    # traceback.print_exc()
    digest = 'null'
    result = float('inf')
  if not math.isinf(result):
    print("  >> [*] Param_entity on sid = %s: config = '%s', tpr = `%.6f`, digest = `%s`, mem_occupy = %d %%" % (dir_sid, config_str_short, result, digest, compute_mem_ratio(result)))

  def progress(percent, width=50):
    percent = min(percent, 100)
    show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * "#")
    progress_print('\r%s %d%%' % (show_str, percent), end='')

  if use_progress:
    with threading.Lock():
      AntaresGlobal.completed_trials += 1
      progress(AntaresGlobal.completed_trials * 1e2 / AntaresGlobal.num_trials)
  return result

def main_compute(code_only=False):
  default_tune_op = importlib.import_module('lang.generic')

  import logging
  import warnings

  warnings.simplefilter("ignore")
  default_tune_op.load_template_op()

  task = Mock()
  task.flop = 0
  for ast in AntaresGlobal.compute_graph[0]:
    local_flop = product([x['range'] for x in ast['props']['data_axes']])
    if ast['props']['reduce_type']:
      local_flop *= 2 * product([x['range'] for x in ast['props']['reduce_axes']])
    task.flop += local_flop

  AntaresGlobal.default_tune_op = default_tune_op
  AntaresGlobal.default_task = task

  if verbose:
    print('  >> Backend = %s, Python PID = %s, Task = %s;' % (backend, os.getpid(), default_tune_op.__name__))

  num_trials = int(os.environ['STEP']) if 'STEP' in os.environ else 0

  config = os.environ.get('CONFIG', '').strip()
  if config != '':
    best_config = config
  elif num_trials > 0:
    dev_num = backend_config.get_execution_parallism()
    if dev_num <= 0:
        raise Exception("No valid device found for backend: %s." % backend)
    batch_size = os.environ.get('BATCH', '')
    batch_size = 16 if not batch_size else int(batch_size)

    from concurrent.futures import ThreadPoolExecutor
    worker_size = batch_size if batch_size < dev_num else dev_num
    thread_pool = ThreadPoolExecutor(max_workers=worker_size)

    tuner_type = 'OpEvo'
    print('  >> MAKE_PARA = %d/%d, EXEC_PARA = %d, TUNER = %s' % (worker_size, batch_size, dev_num, tuner_type))
    print('  >> COMPUTE_V1 = %s\n' % os.environ['COMPUTE_V1'])

    auto_commit = os.environ.get('COMMIT', '')
    if auto_commit:
      saved_code = codehub_db(os.environ['COMPUTE_V1'])
      if saved_code is not None and auto_commit != 'force':
        raise Exception("Saved code has existed in codehub. Please try COMMIT=force to override it.")
      # Avoid child tasks to commit codes
      os.environ.pop('COMMIT')

    try:
      task.search_space_v2 = backend_config.to_search_space(*AntaresGlobal.compute_graph)
      task.n_parallel = batch_size
      tuner = importlib.import_module('tuner.%s.main' % tuner_type)
      tuner = tuner.MainTuner(task)
    except:
      raise Exception('>> Cannot import Antares Tuner: %s' % tuner_type)

    if hasattr(tuner, 'cleanup'):
      AntaresGlobal.cleanup_funcs.append(tuner.cleanup)

    if tuner is not None:
      AntaresGlobal.current_step = 0
      AntaresGlobal.completed_trials = 0
      AntaresGlobal.num_trials = num_trials

      eval_client.init(backend_root=backend_root)

      def measure_batch(inputs):
        results, futures = [], []
        target_sources, config_strs = [], []
        for i in range(len(inputs)):
          dir_sid = AntaresGlobal.current_step + i + 1
          config_str = inputs[i].config if type(inputs[i].config).__name__ == 'str' else 'null'
          config_strs.append(config_str)
          try:
            target_source = get_target_source(config_strs[i], dir_sid)
          except:
            # traceback.print_exc()
            target_source = None
          target_sources.append(target_source)

        expected_timecost = tuner.task.best.timecost if not math.isinf(tuner.task.best.timecost) else min(30, float(os.environ.get('EXPECTED_TIMEOUT', 'inf')))
        for i in range(len(inputs)):
          dir_sid = AntaresGlobal.current_step + i + 1
          futures.append(thread_pool.submit(run_config_entity, target_sources[i], config_strs[i], dir_sid, expected_timecost, i % dev_num))

        best_slot, best_index, best_cost = -1, -1, -1
        for i in range(len(inputs)):
          dir_sid = AntaresGlobal.current_step + i + 1
          t = futures[i].result()
          if t < tuner.task.best.timecost:
            best_slot, best_index, best_cost = dir_sid, i, t
            tuner.task.best.timecost = t
            tuner.task.best.config = inputs[i].config
            tuner.task.best.occur = best_slot
          results.append({"costs": t, "local_id": i, "timestamp": time.time()})
        AntaresGlobal.current_step += len(results)

        stage_logs = 'STEP[%d / %d] Current Best Config = %s, Perf = %g sec / op (%g Gflops), MemRatio = %g %%, Occur Step = %d;' % (
          AntaresGlobal.current_step, num_trials,
          tuner.task.best.config,
          tuner.task.best.timecost, compute_gflops(tuner.task.flop, tuner.task.best.timecost),
          compute_mem_ratio(tuner.task.best.timecost),
          tuner.task.best.occur)

        print('\n\033[93m%s\033[0m' % ('=' * min(120, len(stage_logs))))
        print(stage_logs)
        print('\033[93m%s\033[0m\n' % ('=' * min(120, len(stage_logs))))

        if best_index >= 0:
          tuner.task.best.code = target_sources[best_index][0] + code_suffix(tpr=best_cost, step_prod=best_slot, step_plan=num_trials)
          save_to_path_if_necessary(tuner.task.best.code)

          if auto_commit:
            kernel_path = codehub_db(os.environ['COMPUTE_V1'], source_code=tuner.task.best.code)
            print('  >> Update current code to codehub: %s' % kernel_path)

        return results

      tuner.task.best = Mock()
      tuner.task.best.timecost = float('inf')
      tuner.task.best.config = None
      tuner.task.best.occur = -1

      tuner.measure_batch = measure_batch
      tuner.measure_batch.n_parallel = batch_size
      callbacks = []

      tuner.tune(n_trial=num_trials, callbacks=callbacks, measure_option=None)

      if math.isinf(tuner.task.best.timecost):
        print(f'[Error] No valid config found in the whole tuning. (Try other tuner types other than `TUNER={tuner_type}`?)')
        cleanup_on_exit(0, None)

      best_config = tuner.task.best.config

      if hasattr(tuner.task.best, 'code'):
        tuner.task.best.code += '\n// Antares Tuning Completed in %d steps.' % AntaresGlobal.current_step
        save_to_path_if_necessary(tuner.task.best.code)

        if auto_commit:
          codehub_db(os.environ['COMPUTE_V1'], source_code=tuner.task.best.code)

      print("\n[Best Config] CONFIG='%s'  ==>  Performance is up to %f Gflops, occurred at step %d / %d; time per run = %g sec." % (
        best_config,
        compute_gflops(tuner.task.flop, tuner.task.best.timecost),
        tuner.task.best.occur,
        num_trials,
        tuner.task.best.timecost))

      cleanup_on_exit(-1, None)
    else:
      raise Exception('Unrecognized tuner type: `%s`' % tuner_type)
    exit(0)
  else:
    saved_code = codehub_db(os.environ['COMPUTE_V1'])
    if saved_code is not None:
      print("  >> Using Saved Code from Codehub:")
      print("// ---------------------------------------------------------------------------")
      print(saved_code)
      print("// ---------------------------------------------------------------------------")
      save_to_path_if_necessary(saved_code)
      exit(0)
    best_config = ''

  assert isinstance(best_config, str)

  best_config = best_config if best_config else 'null'
  device_source, kernel_path = get_target_source(best_config)

  if code_only:
    return device_source

  if verbose:
    print()
    print("// ---------------------------------------------------------------------------")
    print(device_source)
    print("// ---------------------------------------------------------------------------")

  save_to_path_if_necessary(device_source)
  eval_client.init(backend_root=backend_root)
  dev_id = int(os.environ.get('DEV_ID', '0'))
  result = evaluate_perf(kernel_path, dev_id, device_source)
  exit(0 if result is not None and len(result) > 1 else 1)


def rest_service():
  import tornado
  import tornado.httpserver
  import tornado.ioloop
  import tornado.web

  task_lists = collections.deque()

  def clear_environ(compute_exp, step):
      os.environ['COMPUTE_V1'] = compute_exp
      os.environ['STEP'] = str(step)
      os.environ['COMMIT'] = 'force'

  class IndexHandler(tornado.web.RequestHandler):
      @tornado.gen.coroutine
      def get(self):
        compute_exp = self.request.headers.get('COMPUTE_V1', '')
        num_step = self.request.headers.get('STEP', '')
        print(">> New connection from peer: `%s` (step = %s)" % (compute_exp, num_step))

        if num_step == '@':
          code = '\n'.join(['Steps: %d; Exprs: %s' % (s, c) for s, c in task_lists])
        elif num_step not in ('', '0'):
          task = (int(num_step), compute_exp)
          if task not in task_lists:
            task_lists.append(task)
          codehub_db(compute_exp, erase=True)
          code = '[Async Task Has Been Put in Background ..]'
        else:
          code = codehub_db(compute_exp)
          duplicate_items = [(s, c) for s, c in task_lists if c == compute_exp]

          if code is None:
            clear_environ(compute_exp, 0)
            try:
              code = main_compute(code_only=True)
              if duplicate_items:
                code += code_suffix(tpr=-1.0, step_prod=0, step_plan=duplicate_items[0][0])
            except:
              print('>> Kernel code failed to generate.')
              code = '[ERROR] ' + traceback.format_exc()
          elif '// Antares Tuning Completed in' not in code and not duplicate_items:
              code = code[:code.rindex('\n// Saved Perf')]
        self.write(code)
        self.flush()
        print(">> Finish subprocess.")
        # yield tornado.gen.sleep(2)

  app = tornado.web.Application([
        (r"/", IndexHandler),
      ],
      cookie_secret = str(random.random()),
      debug = False,
  )
  app.port = int(os.environ.get('HTTP_PORT', '8880'))

  print("* Antares service for backend = `%s` is listening on ':%d'" % (backend, app.port))
  try:
    tornado.httpserver.HTTPServer(app).listen(app.port)
  except Exception as ex:
    raise Exception("Error: %s.\n\nService Failure: Is another process listening on TCP-port %d? Try setting another port with: export HTTP_PORT=<port-num>" % (ex, app.port))

  def scan_tasks(ioloop):
      try:
        if os.wait3(os.WNOHANG)[0] != 0:
          task_lists.popleft()
          raise ChildProcessError
        ## Still waiting for current task to complete
      except ChildProcessError:
        if task_lists:
          task_step, task_expr = task_lists[0]
          clear_environ(task_expr, task_step)
          os.environ['HTTP_SERVICE'], _ = '', os.environ['HTTP_SERVICE']
          os.spawnlp(os.P_NOWAIT, '/bin/bash', 'bash', '%s/run.sh' % compiler_path)
          os.environ['HTTP_SERVICE'] = _
      ioloop.add_timeout(time.time() + 5, lambda: scan_tasks(ioloop))

  ioloop = tornado.ioloop.IOLoop.current()
  scan_tasks(ioloop)
  ioloop.start()


if __name__ == '__main__':
  try:
    if os.environ.get('HTTP_SERVICE', ''):
      rest_service()
    else:
      main_compute()
  except SystemExit:
    cleanup_on_exit(0, None)
  except:
    traceback.print_exc()
