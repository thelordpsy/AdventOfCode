# Less proud of this one.  Written in haste

import re
# [1518-03-02 23:58] Guard #3229 begins shift
# [1518-03-02 00:00] falls asleep
# [1518-03-02 00:01]  wakes up

class ShiftRecords(object):
    __begins_shift = re.compile(r"\[1518-\d\d-\d\d \d\d:\d\d\] Guard #(\d+) begins shift")
    __falls_asleep = re.compile(r"\[1518-\d\d-\d\d \d\d:(\d\d)\] falls asleep")
    __wakes_up = re.compile(r"\[1518-\d\d-\d\d \d\d:(\d\d)\] wakes up")

    def __init__(self):
        self._shifts = {}
        self._current_shift = None

    def process_line(self, line):
        match = ShiftRecords.__begins_shift.match(line)
        if match:
            self._process_begin_shift(match)
            return

        match = ShiftRecords.__falls_asleep.match(line)
        if match:
            self._process_fall_asleep(match)
            return

        match = ShiftRecords.__wakes_up.match(line)
        if match:
            self._process_wake_up(match)
            return

    def _process_begin_shift(self, match):
        guard_id = match.group(1)
        if guard_id not in self._shifts:
            self._shifts[guard_id] = []

        self._shifts[guard_id].append([])
        self._current_shift = self._shifts[guard_id][-1]
        #print("Begin|{}".format(match.group(1)))

    def _process_fall_asleep(self, match):
        asleep_time = match.group(1)
        self._current_shift += [("asleep", int(asleep_time))]
        #print("Asleep|{}".format(match.group(1)))

    def _process_wake_up(self, match):
        awake_time = match.group(1)
        self._current_shift += [("awake", int(awake_time))]
        #print("Awake|{}".format(match.group(1)))


records = ShiftRecords()
with open("input_file.txt", "r") as file:
    for line in sorted(file):
        records.process_line(line)


all_minutes = []

for guard, shifts in records._shifts.items():
    minutes = [0 for i in range(60)]
    for shift in shifts:
        #print(shift)
        start = 0
        state = 0
        try:
            next_transition = shift.pop(0)
            while next_transition:
                #print(start, next_transition[1], state)
                for i in range(start, next_transition[1]):
                    minutes[i] += state
                start = next_transition[1]
                if state == 0:
                    state = 1
                else:
                    state = 0

                next_transition = shift.pop(0)
        except IndexError:
            next_transition = None

        #print(start, 60, state)
        for i in range(start, 60):
            minutes[i] += state

    all_minutes += [(guard, i, minutes[i]) for i in range(60)]


print(all_minutes)
minute = max(all_minutes, key=lambda x:x[2])
print(int(minute[0]) * minute[1])
