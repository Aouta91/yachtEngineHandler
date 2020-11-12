import numpy as np
import pytest

from gps_track import GpsTrack


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
    track = GpsTrack(track_limit=max_sz)
    for i in range(6):
        track((i, i))
    assert len(track) == max_sz


def test_accuracy():
    track = GpsTrack(gps_accuracy=2)
    test_track_data = [(0.5, 1.), [0.5, 0.9], np.asarray([5, 4.]), (5.1, 4.2)]
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
    track = GpsTrack(track_limit=2)
    assert track.get_home() is None
    test_track_data = [(0.5, 1.), [0.7, 0.9], np.asarray([5, 4.]), (5.1, 4.2)]
    for p in test_track_data:
        track(p)
    assert track.get_home() == test_track_data[0]
    track.clear()
    assert track.get_home() is None


def test_dist_to_home():
    track = GpsTrack(track_limit=2)
    assert track.get_home() is None
    test_track_data = [(0.5, 1.), (0.7, 0.9), (5, 4.), (5.1, 4.2), (0, 0), (-4, 3)]
    for p in test_track_data:
        track(p)
    to_home, total = track.get_distance()
    assert to_home == track.euclid_distance(test_track_data[0], test_track_data[-1])
    target_total = 0.
    for i in range(1, len(test_track_data)):
        target_total += track.euclid_distance(test_track_data[i], test_track_data[i - 1])
    assert total == target_total
