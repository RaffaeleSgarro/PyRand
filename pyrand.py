#! /usr/bin/env python
# encoding: utf-8

# PyRand A simple program to randomly assign tasks to people.
#   It takes care to read a input YAML file containing a list
#   of workers and tasks and randomly assigns tasks to each person.
#   If the number of tasks is bigger than the workers one
#   it starts assigning more tasks to each person (always randomly)
#   but taking care to avoid assigning the same people more tasks
#   if someone other has a minor number of tasks.
#   This way it will assure everyone will have random tasks and
#   if the tasks number is a muliplier of the number of workers then
#   workers will always have the same number of tasks, and also if 
#   it's not a multiplier it assures that nobody gets, say 3 tasks
#   while all others have only 1.
#
#   If tasks are less than workers it randomly discards some worker
#   printing a nice message to leave it at home.
#
# Dependencies:
#  *) PyYAML - used to get the input lists in a fashion way
#
# Usage:
#  Fill a YAML file using the following schema:
#
#  tasks:
#    - task1
#    - task2
#    - task3
#    - task4
#  workers:
#    - raffaele
#    - alessandro
#    - guido
#    - python
#
#  Then run 'python pyrand.py FILE.yml' and wait for the output.

import sys
import random
import yaml

def choose_worker(res_dict):
  """Return the key corresponding to the smallest set.
  The last one in case of duplicated.
  """

  ret_me = ""
  ret_me_length = -1

  for k, v in res_dict.iteritems():
    if len(v) < ret_me_length or ret_me_length == -1:
      ret_me_length = len(v)
      ret_me = k
  
  return (ret_me, ret_me_length)

def assign(input_file):
  with open(input_file, "r") as fd:
    perform_assignments(yaml.load(fd.read()))

def perform_assignments(yml_dict):
  try:
    workers = yml_dict["workers"]
    tasks   = yml_dict["tasks"]
  except KeyError:
    sys.stderr.write("Hmm... something went wrong parsing the file.\n")
    sys.stderr.write("Please follow the right schema.")
    exit(1)

  if len(workers) < 1:
    sys.stderr.write("Nobody wants to work anymore nowadays...")
    exit(1)
  
  if len(tasks) < 1:
    sys.stderr.write("Aww... no tasks available for you guys")
    exit(1)

  if len(workers) > len(tasks):
    sys.stdout.write("Somebody will stay at home today...\n")
    while len(workers) > len(tasks):
      print(" *) " + str(workers.pop(random.randrange(len(workers))) + " lost his job today."))
  elif len(tasks) > len(workers):
    print("Somebody will work twice today...")

  res = {}
  for worker in workers:
    res[worker] = []

  # additional takss will be assigned randomly
  additional_tasks = len(tasks)%len(workers)
  
  while (len(tasks) - additional_tasks) > 0:
    task = tasks.pop(random.randrange(len(tasks)))
    res[choose_worker(res)[0]].append(task)

  while additional_tasks:
    # do not assign other tasks to people having already one more than others
    person = random.choice(res.keys())
    if len(res[person]) > choose_worker(res)[1]:
      person = choose_worker(res)[0]

    task = tasks.pop(random.randrange(len(tasks)))
    res[person].append(task)
    additional_tasks -= 1

  print(res)

if __name__ == "__main__":  
  if len(sys.argv) != 2:
    sys.stderr.write("You must at least and only provide the YAML file name.\nRead source comments for info.")
    exit(1)  
  assign(sys.argv[1])
