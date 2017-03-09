from math import pi

from numpy import array, where


def dist_angles(current, target):
    dst = array(current) - array(target)
    while (dst < -pi).any():
        dst[where(dst < -pi)] += 2 * pi
    while (dst > pi).any():
        dst[where(dst > pi)] -= 2 * pi
    return dst


def dist_angle(current, target):
    dst = current - target
    while dst < -pi:
        dst += 2 * pi
    while dst > pi:
        dst -= 2 * pi
    return dst
