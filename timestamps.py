import time

class TimeTracker:
    def __init__(self):
        self.in_between_time = []
        self.previous_time = None

    def get_current_timestamp(self):
        return time.time() * 1000

    def log_time_difference(self):
        current_time = self.get_current_timestamp()
        if self.previous_time is not None:
            time_diff = current_time - self.previous_time
            self.in_between_time.append(time_diff)
        self.previous_time = current_time

    def get_time_average(self):
        if len(self.in_between_time) == 0:
            return 60
        return sum(self.in_between_time) / len(self.in_between_time)

    def get_bpm(self):
        if self.get_time_average() == 0:
            return 0
        return (60/self.get_time_average())/ 1000

