from collections import deque
import numpy as np


DIST_PER_LATITUDE_DEGREE = 62238
DIST_PER_LONGITUDE_DEGREE = 111300


class GpsTrack:

    def __init__(self, gps_accuracy=1e-2, track_limit=None,
                 coord2distance=(DIST_PER_LATITUDE_DEGREE, DIST_PER_LONGITUDE_DEGREE)):
        self._track = deque()
        self._idx = 0
        self._size_limit = track_limit
        self._position_accuracy = gps_accuracy
        self._degree2m = coord2distance
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
        if (len(self._track) > 1) and (self.euclid_distance(self._track[-1], (x, y)) < self._position_accuracy):
            self._dist_total -= self.geograph_distance(self._track[-1], self._track[-2])
            self._track.pop()
        self._track.append((x, y))
        if len(self) == 1:
            self._home = self._track[0]
        if len(self) > 1:
            self._dist_total += self.geograph_distance(self._track[-1], self._track[-2])
        self._dist_to_home = self.geograph_distance(self._track[-1], self._home)
        if self._size_limit is not None:
            if len(self._track) > self._size_limit:
                self._track.popleft()

    def clear(self):
        self._track.clear()
        self._dist_total = 0.
        self._dist_to_home = 0.
        self._home = None

    def get_track(self):
        return self._track

    def get_distance(self):
        return self._dist_to_home, self._dist_total

    def get_home(self):
        return self._home

    def get_current(self):
        return self._track[-1] if len(self) else None

    @staticmethod
    def euclid_distance(p0, p1):
        return np.linalg.norm(np.asarray(p0) - np.asarray(p1))

    @staticmethod
    def geograph_distance(p0, p1):
        return np.sqrt(np.power(DIST_PER_LATITUDE_DEGREE * (p0[0] - p1[0]), 2) +
                       np.power(DIST_PER_LONGITUDE_DEGREE * (p0[1] - p1[1]), 2))


