import numpy as np
import pytest

from gps_track import GpsTrack
from utils import geograph_distance


def test_basic():
    track = GpsTrack()
    assert len(track) == 0
    test_track_data = [(0.5, 1.), (0.7, 0.9), (5, 4.), (-2., 0)]
    for p in test_track_data:
        track(p)
    assert len(track) == len(test_track_data)
    for (target_x, target_y), (x, y) in zip(test_track_data, track):
        assert x == target_x
        assert y == target_y
    track.clear()
    assert len(track) == 0


def test_limit_length():
    max_sz = 3
    track = GpsTrack(track_length_limit=max_sz)
    for i in range(6):
        track((i, i))
    assert len(track) == max_sz


def test_accuracy():
    track = GpsTrack(gps_accuracy_meters=1e5)
    test_track_data = [(45.5, 1.), [45.5, 0.9], np.asarray([55, 4.]), (55.1, 4.2)]
    for p in test_track_data:
        track(p)
    assert len(track) == 3
    x_target, y_target = test_track_data[3]
    assert track[2] == (x_target, y_target)
    x_target, y_target = test_track_data[1]
    assert track[1] == (x_target, y_target)


def test_bad_argument():
    track = GpsTrack()
    with pytest.raises(TypeError):
        track("Bad point")
    with pytest.raises(TypeError):
        track(1)
    with pytest.raises(ValueError):
        track((1, "S"))


def test_home():
    track = GpsTrack(track_length_limit=2)
    assert track.get_home() is None
    test_track_data = [(0.5, 1.), [0.7, 0.9], np.asarray([5, 4.]), (5.1, 4.2)]
    for p in test_track_data:
        track(p)
    assert track.get_home() == test_track_data[0]
    track.clear()
    assert track.get_home() is None


def test_dist():
    track = GpsTrack(track_length_limit=2)
    assert track.get_home() is None
    test_track_data = [(45.5, 41.), (45.7, 41.9), (45, 41.), (45.1, 41.2), (40, 40), (44, 41)]
    for p in test_track_data:
        track(p)
    to_home, total = track.get_distance()
    assert to_home == geograph_distance(test_track_data[0], test_track_data[-1])
    target_total = 0.
    for i in range(1, len(test_track_data)):
        target_total += geograph_distance(test_track_data[i], test_track_data[i - 1])
    assert total == pytest.approx(target_total, 1000)


def test_sresample_track():
    pts = [(0., 0.), (0, 5), (0, 10), (5, 10), (10, 10), (10, 5), (10, 0)]
    target = [(0., 0.), (0, 10), (10, 10), (10, 0)]
    track = GpsTrack(gps_accuracy_meters=10, track_length_limit=None)
    for p in pts:
        track(p)

    tr = track.get_track(len(target))
    assert len(tr) == len(target)
    for (x, y), (tx, ty) in zip(tr, target):
        assert abs(x - tx) < 0.1
        assert abs(y - ty) < 0.1

    target = [(0., 0.), (5, 10), (10, 0)]
    tr = track.get_track(len(target))
    assert len(tr) == len(target)
    for (x, y), (tx, ty) in zip(tr, target):
        assert abs(x - tx) < 0.1
        assert abs(y - ty) < 0.1
