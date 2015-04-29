from math import pi
def dist_angles(actuel, cible):
    dst = actuel - cible
    while dst < -pi:
        dst += 2 * pi
    while dst > pi:
        dst -= 2 * pi
    return dst

