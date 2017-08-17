from math import pi, tau

from numpy import array, where


def dist_angles(current, target):
    dst = array(current) - array(target)
    while (dst < -pi).any():
        dst[where(dst < -pi)] += tau
    while (dst > pi).any():
        dst[where(dst > pi)] -= tau
    return dst


def dist_angle(current, target):
    dst = current - target
    while dst < -pi:
        dst += tau
    while dst > pi:
        dst -= tau
    return dst
