import random
import itertools

def assign(tasks, assignees):
  tasks = list(tasks)
  assignees = list(assignees)
  random.shuffle(tasks)
  random.shuffle(assignees)
   
  assignments = {}
    
  for assignee in assignees:
    assignments[assignee] = list()
    
  # Act as a round-robin (circular, infinite) list
  assignees = itertools.cycle(assignees)
    
  for task in tasks:
    assignments[assignees.next()].append(task)
    
  return assignments

