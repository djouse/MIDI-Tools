import time

class Bpm:
    def __init__(self, bpm):
        self.space_between_beats = 0.5
        self.last_press = time.time()
        self.bpm = bpm
        self.times = []
        self._last_update = time.time()
        self._elapsed_time = 0.0
        self._last_closeness = 1.0
        self.on_beat = 0
        self.beat_num = 0
        self.finished_beat = 0
        self.first_beat = 0
        self.started_beat = 0
    
    def setBpm(self, bpm):
        self.bpm=bpm

    def update(self):
        the_time = time.time()
        self._elapsed_time += the_time - self._last_update
        self._last_update = the_time

        space_between_beats = 60.0 / self.bpm
        since_last_beat = the_time - self.on_beat

        self.finished_beat = self.on_beat and (since_last_beat > 0.1)
        if self.finished_beat:
            self.on_beat = 0

        closeness = self._elapsed_time % space_between_beats
        if closeness < self._last_closeness:
            self.on_beat = the_time
            self.finished_beat = 0
            self.beat_num += 1
            self.started_beat = 1
            self.first_beat = not (self.beat_num % 4)
        else:
            self.started_beat = 0

        self._last_closeness = closeness