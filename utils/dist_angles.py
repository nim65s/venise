from math import pi

from numpy import array, where


def dist_angles(actuel, cible):
    dst = array(actuel) - array(cible)
    while (dst < -pi).any():
        dst[where(dst < -pi)] += 2 * pi
    while (dst > pi).any():
        dst[where(dst > pi)] -= 2 * pi
    return dst


def dist_angle(actuel, cible):
    dst = actuel - cible
    while dst < -pi:
        dst += 2 * pi
    while dst > pi:
        dst -= 2 * pi
    return dst
