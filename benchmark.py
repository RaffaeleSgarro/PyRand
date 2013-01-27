import yaml
import raf
import alex
import sys
import time
import pprint

def main(filename):
  with open(filename, "r") as fd:
    data = yaml.load(fd.read())

    implementations = {
      "Raffaele": raf.assign,
      "Alessandro": alex.assign
    }
    
    stat(implementations, data)

# Collect statistics of interleaved runs
#  impls is a map label -> function, data is the yaml database
def stat (impls, data):
  for label, f in impls.items():
    times = 100000
    start = time_millis()
    series = list()
    for i in range(times):
      assignments = f(data["tasks"], data["workers"])
      series.append(assignments)
    duration = time_millis() - start
    print "%s took %dms, %.2fms on average" % (label, duration, float(duration) / times)
    examine_result(series, data)

# Looks baaaaaaaaaaaaad there must be a library for this    
def examine_result(result, data):
  
  work = dict()
  for assignee in data["workers"]:
    work[assignee] = 0
  
  work2 = dict()
  for task in data["tasks"]:
    work2[task] = dict()
    for worker in data["workers"]:
      work2[task][worker] = 0
  
  for entry in result:
    for assignee, tasks in entry.items():
      work[assignee] = work[assignee] + len(tasks)
      for task in tasks:
        work2[task][assignee] = work2[task][assignee] + 1
  pprint.pprint(work)
  pprint.pprint(work2)
    
def time_millis():
  return int(round(time.time() * 1000))

if __name__ == "__main__":
  main (sys.argv[1] if len(sys.argv) == 2 else "input.yml")
  
