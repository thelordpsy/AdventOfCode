import re


class Worker(object):
    def __init__(self):
        self._task = None
        self._remaining_time = None

    def take_work(self, graph):
        step = graph.next_step()
        if step:
            self._task = step
            self._remaining_time = 60 + (1 + ord(step) - ord('A'))
            graph.claim(step)

    def advance_time(self, graph):
        if self._remaining_time != None:
            self._remaining_time -= 1
            if self._remaining_time == 0:
                graph.complete(self._task)
                self._task = None
                self._remaining_time = None

class WorkerPool(object):
    def __init__(self, graph):
        self._time_index = 0
        self._workers = [Worker()  for i in range(5)]
        self._graph = graph

    def solve(self):
        while not self._graph.is_finished():
            free_workers = self._free_workers()
            if len(free_workers) == 0:
                self._advance_time()
                continue

            for worker in free_workers:
                worker.take_work(self._graph)

            self._advance_time()
        print("Time Required: {}".format(self._time_index))

    def _free_workers(self):
        return [worker for worker in self._workers if worker._task is None]

    def _advance_time(self):
        self.print_state()
        self._time_index += 1
        for worker in self._workers:
            worker.advance_time(self._graph)

    def print_state(self):
        state = "{}\t".format(self._time_index)
        for worker in self._workers:
            if worker._task != None:
                state += worker._task
            else:
                state += "."
        state += "\t"
        state += "".join(self._graph.completed_steps())
        print(state)


class Step(object):
    def __init__(self, name):
        self.name = name
        self._requirements = []
        self.complete = False
        self.in_progress = False

    def requires(self, requirement):
        self._requirements += requirement

    def can_run(self, completed):
        if self.complete or self.in_progress:
            return False

        for requirement in self._requirements:
            if requirement not in completed:
                return False
        return True

class Graph(object):
    __rule = re.compile("Step (.) must be finished before step (.) can begin.")
    def __init__(self):
        self._steps = {}

    def add_rule(self, line):
        match = Graph.__rule.match(line)
        assert(match)

        first = match.group(1)
        second = match.group(2)

        if first not in self._steps:
            self._steps[first] = Step(first)
        if second not in self._steps:
            self._steps[second] = Step(second)

        self._steps[second].requires(first)

    def claim(self, step):
        assert(not self._steps[step].in_progress)
        assert(not self._steps[step].complete)
        self._steps[step].in_progress = True

    def complete(self, step):
        assert(self._steps[step].in_progress)
        assert(not self._steps[step].complete)
        self._steps[step].complete = True

    def completed_steps(self):
        return [step_name for step_name, step in self._steps.items() if step.complete]

    def can_run(self):
        return [step_name for step_name, step in self._steps.items() if step.can_run(self.completed_steps())]

    def next_step(self):
        available_work = self.can_run()
        if len(available_work) != 0:
            return sorted(available_work)[0]
        return None

    def is_finished(self):
        for step_name, step in self._steps.items():
            if not step.complete:
                return False
        return True


graph = Graph()
with open("input_file.txt") as file:
    for line in file:
        graph.add_rule(line)

worker_pool = WorkerPool(graph)
worker_pool.solve()