PyRand allocates tasks among assignees.

It reads the input lists from a YAML file named on the command line.
The tasks are not prioritized in any way, and are assumed to be a
homogeneous set of atomic pieces of work.

The program distributes them randomly, and ensures that everyone is
assigned the same number of tasks. If the latter is not possible, it
still guarantees that the difference between the most loaded worker
and the least loaded one is no more than 1 task.
