from numpy import arccos, array, dot, pi
from numpy.linalg import det, norm


def dist_seg(a, b, p):
    """ segment line ab, point p, where each one is an array([x, y]) """
    a, b, p = map(array, [a, b, p])
    if all(a == p) or all(b == p):
        return 0
    if arccos(min(dot((p - a) / norm(p - a), (b - a) / norm(b - a)), 1)) > pi / 2:
        return norm(p - a)
    if arccos(min(dot((p - b) / norm(p - b), (a - b) / norm(a - b)), 1)) > pi / 2:
        return norm(p - b)
    return abs(dot(a - b, p[::-1]) + det([a, b])) / norm(a - b)


def dist_path(path, point):
    return min([dist_seg(path[i], path[(i + 1) % len(path)], point) for i in range(len(path))])
