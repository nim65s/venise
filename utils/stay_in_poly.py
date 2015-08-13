from numpy import array, cross


def inter(a, b, ap, bp):
    """ [a b] ∩ [ap bp] ? """
    a, b, ap, bp = map(array, [a, b, ap, bp])
    if cross(b - a, bp - ap) == 0:  # segments parallèles
        return False
    if cross(b - a, bp - a) * cross(b - a, ap - a) > 0:  # point d’intersection pas entre ap et bp
        return False
    if cross(bp - ap, b - ap) * cross(bp - ap, a - ap) > 0:  # point d’intersection pas entre a et b
        return False
    return True


def stay_in_poly(pos, dest, bord):
    """ ne sort (*ou rentre*) pas dans le polygone """
    return all([not inter(pos, dest, bord[i], bord[(i + 1) % len(bord)]) for i in range(len(bord))])
