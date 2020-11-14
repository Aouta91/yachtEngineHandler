from geopy import distance


def geograph_distance(p0, p1):
    return distance.distance(p0, p1).m