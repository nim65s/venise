# -*- coding: utf-8 -*-
from enum import IntEnum
from math import pi, sin, cos
from socket import gethostname

from numpy import array, cos, sin, pi

# Constantes AGV
RAYON_AGV = 1.180
POS_ROUES = [-pi / 4, pi / 4, pi]

# Constantes Tourelles
VIT_MOY_MAX = 16.5  # mm / s

# δt
PERIODE = 0.1

# TCP AGV
HOST_AGV = '192.168.1.10'
PORT_AGV = 8001
PORT_UBISENS = 1336
PORT_ENTREES = 1337
PORT_SORTIES = 1338
PORT_CACHE = 1339
PORT_TIM = 2112  # TODO: y’en aura deux sur les AGV, et pour les tests y’a un HOST différent…

N_SONDES = 3  # par arbre

# On veut faire faire pi/2 en 50 cm, si on est à vitesse max
SMOOTH_FACTOR = pi / 2 / (60 * 0.5 / PERIODE)

# Position des murs
ANGLES = [[8, 7], [8, 8], [11, 14], [13, 17], [14.5, 17.5], [16, 17], [17, 16], [20, 14], [27, 14], [30, 16], [31, 17], [33, 17], [34, 16], [34, 15], [32, 13], [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [10, 6.5], [9, 6.5]]
MURS = [[a, ANGLES[i + 1] if i + 1 < len(ANGLES) else ANGLES[0]] for i, a in enumerate(ANGLES)]
_N = 24
#INTERIEUR = [[-14, 4.5], [-14, 13.5], [-5, 13.5], [-5, 4.5]]
INTERIEUR = [(3 * cos(i * pi / _N) - 9, 3 * sin(i * pi / _N) + 9) for i in range(2 * _N)]

PATH_EXT = [[8.5, 7], [13, 17], [16, 17], [20, 13.5], [27, 13.5], [32, 17], [25, 9], [25, 4], [20, 4], [15, 8]]

_a, _i = array(ANGLES), array(INTERIEUR)
(MIN_X, MIN_Y), (MAX_X, MAX_Y) = _a.min(axis=0) - 0.5, _a.max(axis=0) + 0.5
(MIN_X_INT, MIN_Y_INT), (MAX_X_INT, MAX_Y_INT) = _i.min(axis=0) - 0.5, _i.max(axis=0) + 0.5

# SVG
WIDTH = 35 + 15
HEIGHT = 20
PX_PAR_M = 35
POINTS_SVG = _a * PX_PAR_M
INTERIEUR_SVG = _i * PX_PAR_M
ANTENNES = array([
    [-15.4, 3.26],
    [-3.89, 3.15],
    [-3.9, 14.65],
    [0.55, 0.28],
    [2.67, 13.34],
    [13.54, 25.98],
    [33.95, 25.85],
    [28.39, 5.36],
    ]) * PX_PAR_M
PATH_EXT_SVG = array(PATH_EXT) * PX_PAR_M


Hote = IntEnum('Hôte', 'cerf moro ame yuki')
try:
    CURRENT_HOST = Hote[gethostname().split('.')[0].lower()]
except KeyError:
    CURRENT_HOST = Hote.cerf
MAIN_HOST = Hote.cerf

BERCAIL = {
        Hote.moro: (0, 0),
        Hote.ame: (8, 6),
        Hote.yuki: (9, 11),
        }
