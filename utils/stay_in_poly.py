from math import atan2, cos, pi, sin

from numpy import array, cross

from .point_in_polygon import wn_pn_poly


def inter(a, b, ap, bp, strict=True):
    """ [a b] ∩ [ap bp] ? """
    a, b, ap, bp = map(array, [a, b, ap, bp])
    if cross(b - a, bp - ap) == 0:  # segments parallèles
        return False
    if cross(b - a, bp - a) * cross(b - a, ap - a) > 0:  # point d’intersection pas entre ap et bp
        return False
    if cross(bp - ap, b - ap) * cross(bp - ap, a - ap) > 0:  # point d’intersection pas entre a et b
        return False
    if not strict and ((b == ap).all() or (b == bp).all()):
        return False
    return True


def stay_in_poly(pos, dest, bord, margin=0.5, strict=True):
    """ don't cross polygon """
    if not all([not inter(pos, dest, bord[i], bord[(i + 1) % len(bord)], strict=strict) for i in range(len(bord))]):
        return False
    if margin == 0:
        return all([wn_pn_poly(p, bord) for p in [pos, dest]]) if strict else True
    a = atan2(dest[1] - pos[1], dest[0] - pos[0])
    pos_p = pos[0] + margin * cos(a + pi / 2), pos[1] + margin * sin(a + pi / 2)
    dest_p = dest[0] + margin * cos(a + pi / 2), dest[1] + margin * sin(a + pi / 2)
    if not all([not inter(pos_p, dest_p, bord[i], bord[(i + 1) % len(bord)], strict=strict) for i in range(len(bord))]):
        return False
    pos_m = pos[0] + margin * cos(a - pi / 2), pos[1] + margin * sin(a - pi / 2)
    dest_m = dest[0] + margin * cos(a - pi / 2), dest[1] + margin * sin(a - pi / 2)
    if not all([not inter(pos_m, dest_m, bord[i], bord[(i + 1) % len(bord)], strict=strict) for i in range(len(bord))]):
        return False
    return all([wn_pn_poly(p, bord) for p in [pos, pos_p, pos_m, dest, dest_p, dest_m]])
