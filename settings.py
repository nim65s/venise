# -*- coding: utf-8 -*-
from enum import IntEnum
from math import pi
from socket import gethostname

# Scène TODO
MAX_X = 12000
MAX_Y = 12000

# Constantes AGV
RAYON_AGV = 1180
POS_ROUES = [-pi / 4, pi - 4, pi]

# Constantes Tourelles
VIT_MOY_MAX = 16.5  # mm / s
VIT_LIN_MAX = 16.5  # mm / s
ACC_LIN_MAX = 200   # mm / s²
VIT_ANG_MAX = 20 * pi / 180  # rad / s
MAX_TOURS = 280

# δt
PERIODE = 0.1

# TCP AGV
# TODO update var names
AGV_HOST = ['', '127.0.0.1', '192.168.37.48', '192.168.37.49', '192.168.37.50']
AGV_PORT = 8001

ENTREES_HOST = 'localhost'
ENTREES_PORT = 1337
SORTIES_HOST = 'localhost'
SORTIES_PORT = 1338

# web
R_ARBRES = 16
STROKE_WIDTH = 4

# Position intiale des arbres
ARBRES = [
        {'x': 250, 'y': 50, 't': 0, 'u': 0, 'v': 0, 'w': 0},
        {'x': 750, 'y': 250, 't': 90, 'u': 0, 'v': 0, 'w': 0},
        ]
N_SONDES = 4  # par arbre

# Position des murs
ANGLES = [[9, 5], [942, 1], [986, 312], [542, 396], [18, 250]]
MURS = [[a, ANGLES[i + 1] if i + 1 < len(ANGLES) else ANGLES[0]] for i, a in enumerate(ANGLES)]

hosts = IntEnum('Hôte', 'cerf moro ame yuki')
try:
    current_host = hosts[gethostname().split('.')[0].lower()]
except KeyError:
    current_host = hosts.yuki
