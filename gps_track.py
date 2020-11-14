from collections import deque
import numpy as np

from utils import geograph_distance


class GpsTrack:

    def __init__(self, gps_accuracy_meters=10, track_length_limit=None):
        self._track = deque()
        self._distances = deque()
        self._idx = 0
        self._size_limit = track_length_limit
        self._position_accuracy = gps_accuracy_meters
        self._home = None
        self._dist_to_home = 0.
        self._dist_total = 0.

    def __str__(self):
        return "GpsTrack"

    def __call__(self, *args, **kwargs):
        self.add(*args, **kwargs)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._track)

    def __next__(self):
        if self._idx < len(self._track):
            out = self._track[self._idx]
            self._idx += 1
            return out
        else:
            self._idx = 0
            raise StopIteration

    def __getitem__(self, key):
        if type(key) == slice:
            return [self[i] for i in range(*key.indices(len(self)))]
        elif type(key) == int:
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError(f"The index {key} is out of range.")
            return self._track[key]
        else:
            raise TypeError("Invalid argument type.")

    def add(self, point):
        if len(point) != 2:
            raise TypeError("Only 2d coordinates point may be used")
        x, y = float(point[0]), float(point[1])
        if len(self) == 0:
            self._home = (x, y)
            self._track.append((x, y))
            self._distances.append(0.)
            return

        dist_to_tail = geograph_distance(self._track[-1], (x, y))
        while dist_to_tail < self._position_accuracy and len(self) > 1:
            self._dist_total -= geograph_distance(self._track[-1], self._track[-2])
            self._track.pop()
            dist_to_tail = geograph_distance(self._track[-1], (x, y))
        self._track.append((x, y))
        self._distances.append(dist_to_tail + self._distances[-1])
        self._dist_to_home = geograph_distance(self._track[-1], self._home)

        if self._size_limit and len(self) > self._size_limit:
            self._track.popleft()

    def clear(self):
        self._track.clear()
        self._dist_total = 0.
        self._dist_to_home = 0.
        self._home = None

    def get_track(self, max_length=None):
        return self.resample_track(max_length) if max_length else self._track

    def get_distance(self):
        return self._dist_to_home, self._dist_total

    def get_home(self):
        return self._home

    def get_current(self):
        return self._track[-1] if len(self) else None

    def resample_track(self, max_points=8):
        if len(self) <= max_points or len(self) < 3:
            return self._track
        out = [self._track[0]]
        distance_step = self._distances[-1] / (max_points - 1)
        for i in range(1, max_points-1):
            desired_dist = i * distance_step
            left = np.searchsorted(self._distances, desired_dist)
            out.append(self.interpolate_2d(p0=self._track[left], p1=self._track[left + 1],
                                           left=(desired_dist - self._distances[left])))
        out.append(self._track[-1])
        return out

    @staticmethod
    def interpolate_2d(p0, p1, left):
        (x1, y1), (x2, y2) = p0, p1
        k = left / geograph_distance(p0, p1)
        return x1 + k * (x2 - x1), y1 + k * (y2 - y1)
