import re

class Step(object):
    def __init__(self, name):
        self.name = name
        self._requirements = []
        self.complete = False

    def requires(self, requirement):
        self._requirements += requirement

    def can_run(self, completed):
        if self.complete:
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

    def completed_steps(self):
        return [step_name for step_name, step in self._steps.items() if step.complete]

    def can_run(self):
        return [step_name for step_name, step in self._steps.items() if step.can_run(self.completed_steps())]

    def next_step(self):
        return sorted(self.can_run())[0]

    def is_finished(self):
        for step_name, step in self._steps.items():
            if not step.complete:
                return False
        return True

    def solve(self):
        path = []
        while not self.is_finished():
            next_step = self.next_step()
            path += next_step
            self._steps[next_step].complete = True
        print("".join(path))


graph = Graph()
with open("input_file.txt") as file:
    for line in file:
        graph.add_rule(line)
graph.solve()