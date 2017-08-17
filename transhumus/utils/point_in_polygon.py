#!/usr/bin/env python
#
# routine for performing the "point in polygon" inclusion test

# Copyright 2001, softSurfer (www.softsurfer.com)
# This code may be freely used and modified for any purpose
# providing that this copyright notice is included with it.
# SoftSurfer makes no warranty for this code, and cannot be held
# liable for any real or imagined damage resulting from its use.
# Users of this code must verify correctness for their application.

# translated to Python by Maciej Kalisiak <mac@dgp.toronto.edu>

# pep8 by Guilhem Saurel <gsaurel@laas.fr>

#   a Point is represented as a tuple: (x,y)

# ==================================================================

# is_left(): tests if a point is Left|On|Right of an infinite line.

#   Input: three points P0, P1, and P2
#   Return: >0 for P2 left of the line through P0 and P1
#           =0 for P2 on the line
#           <0 for P2 right of the line
#   See: the January 2001 Algorithm "Area of 2D and 3D Triangles and Polygons"


def is_left(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])

# ==================================================================

# cn_pn_poly(): crossing number test for a point in a polygon
#     Input:  P = a point,
#             V[] = vertex points of a polygon
#     Return: 0 = outside, 1 = inside
# This code is patterned after [Franklin, 2000]


def cn_pn_poly_cn(p, v):
    cn = 0    # the crossing number counter

    # repeat the first vertex at end
    v = tuple(v[:]) + (v[0],)

    # loop through all edges of the polygon
    for i in range(len(v) - 1):   # edge from V[i] to V[i+1]
        if ((v[i][1] <= p[1] and v[i + 1][1] > p[1])   # an upward crossing
                or (v[i][1] > p[1] and v[i + 1][1] <= p[1])):  # a downward crossing
            # compute the actual edge-ray intersect x-coordinate
            vt = (p[1] - v[i][1]) / float(v[i + 1][1] - v[i][1])
            if p[0] < v[i][0] + vt * (v[i + 1][0] - v[i][0]):  # P[0] < intersect
                cn += 1  # a valid crossing of y=P[1] right of P[0]
    return cn


def cn_pn_poly(p, v):
    return cn_pn_poly_cn(p, v) % 2   # 0 if even (out), and 1 if odd (in)

# ==================================================================

# wn_pn_poly(): winding number test for a point in a polygon
#     Input:  P = a point,
#             V[] = vertex points of a polygon
#     Return: wn = the winding number (=0 only if P is outside V[])


def wn_pn_poly(p, v):
    wn = 0   # the winding number counter

    # repeat the first vertex at end
    v = tuple(v[:]) + (v[0],)

    # loop through all edges of the polygon
    for i in range(len(v) - 1):     # edge from V[i] to V[i+1]
        if v[i][1] <= p[1]:        # start y <= P[1]
            if v[i + 1][1] > p[1]:     # an upward crossing
                if is_left(v[i], v[i + 1], p) > 0:  # P left of edge
                    wn += 1           # have a valid up intersect
        else:                      # start y > P[1] (no test needed)
            if v[i + 1][1] <= p[1]:    # a downward crossing
                if is_left(v[i], v[i + 1], p) < 0:  # P right of edge
                    wn -= 1           # have a valid down intersect
    return wn
