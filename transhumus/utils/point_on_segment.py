from math import hypot

EPSILON = 0.03


def point_on_segment(a, b, p):
    """ segment line ab, point p, where each one is a (x, y) """
    def dist(m, n):
        return hypot(m[0] - n[0], m[1] - n[1])
    return -EPSILON < dist(a, p) + dist(p, b) - dist(a, b) < EPSILON


def point_on_boundary(pos, boundary):
    return any([point_on_segment(boundary[i], boundary[(i + 1) % len(boundary)], pos) for i in range(len(boundary))])
