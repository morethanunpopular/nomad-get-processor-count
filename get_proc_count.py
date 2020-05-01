#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import logging
import subprocess
import multiprocessing

def get_clock_speed():
  try:
    cmd = "lscpu | grep MHz | awk '{print $3}' | cut -d . -f 1"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
      logging.error(error)
  except Exception as e:
    logging.error("Exception: {}".format(e))
    output = None
  return output



def get_total_clock():
  try:
    core_count = multiprocessing.cpu_count()
    clock_speed = get_clock_speed()
    if clock_speed:
      total_clock = int(core_count) * int(clock_speed)
    else:
      logging.error("Clock speed could not be calculated!")
      total_clock = None
  except Exception as e:
    logging.error("Exception: {}".format(e))
    total_clock = None
  return total_clock

def calculate_functional_procs(allocated_clock):
  try:
    total_clock = float(get_total_clock())
    core_count = float(multiprocessing.cpu_count())
    if total_clock:
      functional_procs = float(allocated_clock) / total_clock * core_count
      output = int(functional_procs)
      if output < 1:
        output = 1
    else:
      output = 0
  except Exception as e:
    logging.error("Exception: {}".format(e))
    output = None
  return output

if __name__ == '__main__':
  try:
    allocated_clock = os.environ.get('NOMAD_CPU_LIMIT')
    if not allocated_clock:
      logging.error("No CPU LIMIT SET!")
      print(0)
      sys.exit(1)
    functional_procs = calculate_functional_procs(int(allocated_clock))
    if functional_procs:
      print(functional_procs)
    else:
      print(0)
  except Exception as e:
    logging.error("Exception: {}".format(e))
    print(0)
