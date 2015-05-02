from math import pi
from numpy import array

def dist_angles(actuel, cible):
    dst = array(actuel) - array(cible)
    while (dst < -pi).any():
        dst[where(dst < -pi)] += 2 * pi
    while (dst > pi).any():
        dst[where(dst > pi)] -= 2 * pi
    return dst

