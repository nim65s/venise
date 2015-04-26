# -*- coding: utf-8 -*-
from enum import IntEnum
from math import pi
from socket import gethostname

from numpy import array

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

# Position intiale des arbres
N_SONDES = 3  # par arbre

# Position des murs
ANGLES = [[8, 7], [8, 8], [11, 14], [13, 17], [14.5, 17.5], [16, 17], [17, 16], [20, 14], [27, 14], [30, 16], [31, 17], [33, 17], [34, 16], [34, 15], [32, 13], [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [10, 6.5], [9, 6.5]]
MURS = [[a, ANGLES[i + 1] if i + 1 < len(ANGLES) else ANGLES[0]] for i, a in enumerate(ANGLES)]
INTERIEUR = [[-14, 4.5], [-14, 13.5], [-5, 13.5], [-5, 4.5]]

_a, _i = array(ANGLES), array(INTERIEUR)
(MIN_X, MIN_Y), (MAX_X, MAX_Y) = _a.min(axis=0) - 0.5, _a.max(axis=0) + 0.5

WIDTH = 35 + 15
HEIGHT = 20

# SVG
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


Hote = IntEnum('Hôte', 'cerf moro ame yuki')
try:
    CURRENT_HOST = Hote[gethostname().split('.')[0].lower()]
except KeyError:
    CURRENT_HOST = Hote.cerf
MAIN_HOST = Hote.cerf
