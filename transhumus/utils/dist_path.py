from numpy import arccos, array, dot, pi
from numpy.linalg import det, norm


def dist_seg(A, B, P):
    """ segment line AB, point P, where each one is an array([x, y]) """
    A, B, P = map(array, [A, B, P])
    if all(A == P) or all(B == P):
        return 0
    if arccos(min(dot((P - A) / norm(P - A), (B - A) / norm(B - A)), 1)) > pi / 2:
        return norm(P - A)
    if arccos(min(dot((P - B) / norm(P - B), (A - B) / norm(A - B)), 1)) > pi / 2:
        return norm(P - B)
    return abs(dot(A - B, P[::-1]) + det([A, B])) / norm(A - B)


def dist_path(path, point):
    return min([dist_seg(path[i], path[(i + 1) % len(path)], point) for i in range(len(path))])
