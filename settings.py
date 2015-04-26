# -*- coding: utf-8 -*-
from enum import IntEnum
from math import pi
from socket import gethostname

from numpy import array

# Scène TODO
MAX_X = 12000
MAX_Y = 12000

# Constantes AGV
RAYON_AGV = 1180
POS_ROUES = [-pi / 4, pi / 4, pi]

# Constantes Tourelles
VIT_MOY_MAX = 16.5  # mm / s

# δt
PERIODE = 0.25

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
ANGLES = [[7, 7], [11, 14], [27, 14], [30, 16], [32, 17], [32, 13], [26, 13], [24, 9], [22, 9]]
_a = array(ANGLES)
MURS = [[a, ANGLES[i + 1] if i + 1 < len(ANGLES) else ANGLES[0]] for i, a in enumerate(ANGLES)]

(MIN_X, MIN_Y), (MAX_X, MAX_Y) = _a.min(axis=0) - 0.5, _a.max(axis=0) + 0.5

Hote = IntEnum('Hôte', 'cerf moro ame yuki')
try:
    CURRENT_HOST = Hote[gethostname().split('.')[0].lower()]
except KeyError:
    CURRENT_HOST = Hote.cerf
MAIN_HOST = Hote.cerf
