from math import hypot

EPSILON = 0.03


def point_on_segment(A, B, P):
    """ segment line AB, point P, where each one is a (x, y) """
    def dist(a, b):
        return hypot(a[0] - b[0], a[1] - b[1])
    return -EPSILON < dist(A, P) + dist(P, B) - dist(A, B) < EPSILON


def point_on_boundary(pos, boundary):
    return any([point_on_segment(boundary[i], boundary[(i + 1) % len(boundary)], pos) for i in range(len(boundary))])
