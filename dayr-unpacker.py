import sys
import subprocess
import time
import os

from pathlib import Path
from queue import Empty as EmptyQueue
from multiprocessing import Process, JoinableQueue, cpu_count
from corona_archive import CoronaArchiver

def unluac(file, args):
  proc = subprocess.run(args, capture_output = True, timeout = 30)
  proc.check_returncode()
  
  return proc.stdout

def worker_func(file_queue):
  unluac_args = [
    'java',
    '-jar',
    'unluac.jar'
  ]
  
  try:
    while True:
      file = file_queue.get(False)
      resfile = os.path.join('res', file)
      args = [*unluac_args, '--disassemble', resfile]
      
      print(f'Disassembling {resfile}...')
      dis_script = unluac(file, args)
      
      path = os.path.splitext(file)[0].split('.')
      name = path[-1]
      path = os.path.join('dis', *path[:-1])
      
      os.makedirs(path, exist_ok = True)
      
      with open(os.path.join(path, name) + '.bc', 'wb') as dis_fobj:
        dis_fobj.write(dis_script)
      
      args = [*unluac_args, resfile]
      
      print(f'Decompiling {resfile}...')
      dec_script = unluac(file, args)
      
      path = os.path.splitext(file)[0].split('.')
      name = path[-1]
      path = os.path.join('src', *path[:-1])
      
      os.makedirs(path, exist_ok = True)
      
      with open(os.path.join(path, name) + '.lua', 'wb') as dec_fobj:
        dec_fobj.write(dec_script)
      
      file_queue.task_done()
  except EmptyQueue:
    print('No more tasks. Worker shutting down.')
    
    return
  except KeyboardInterrupt:
    print('Worker shutting down...')
    
    return

def main(resources, workers):
  worker_processes = []
  file_queue = JoinableQueue()
  
  # ensure the output directories exist
  Path('res').mkdir(exist_ok = True)
  Path('src').mkdir(exist_ok = True)
  Path('dis').mkdir(exist_ok = True)
  
  archiver = CoronaArchiver()
  archiver.unpack(resources, os.path.join('res', ''))
  
  for file in os.listdir('res'):
    file_queue.put(file)
  
  for worker_id in range(workers):
    worker = Process(target = worker_func, args = (file_queue,))
    
    worker_processes.append(worker)
    worker.start()
  
  # wait for all files to be processed
  file_queue.join()

if __name__ == '__main__':
  try:
    main(sys.argv[1], cpu_count() - 1)
  except KeyboardInterrupt:
    pass