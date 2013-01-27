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

def assign(tasks, workers):
  # Don't modify the input lists
  tasks = list(tasks)
  workers = list(workers)
  
  if len(workers) < 1:
    raise Exception("Nobody wants to work anymore nowadays...")
  
  if len(tasks) < 1:
    raise Exception("Aww... no tasks available for you guys")
  
  if len(workers) > len(tasks):
    # sys.stdout.write("Somebody will stay at home today...\n")
    while len(workers) > len(tasks):
      # print(" *) " + str(workers.pop(random.randrange(len(workers))) + " lost his job today."))
      workers.pop(random.randrange(len(workers)))
  elif len(tasks) > len(workers):
    # print("Somebody will work twice today...")
    pass

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

  return res

