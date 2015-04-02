# -*- coding: utf-8 -*-
from enum import IntEnum
from math import pi
from socket import gethostname

# Scène TODO
MAX_X = 12000
MAX_Y = 12000

# Constantes AGV
RAYON_AGV = 1180
POS_ROUES = [-pi / 4, pi / 4, pi]

# Constantes Tourelles
VIT_MOY_MAX = 16.5  # mm / s

# δt
PERIODE = 0.1

# TCP AGV
# TODO update var names
HOST_AGV = ['localhost', 'localhost', '192.168.37.48', '192.168.37.49', '192.168.37.50']
PORT_AGV = 8001
PORT_ENTREES = 1337
PORT_SORTIES = 1338
PORT_TIM = 2112  # TODO: y’en aura deux sur les AGV, et pour les tests y’a un HOST différent…

# web
R_ARBRES = 16
STROKE_WIDTH = 4

# Position intiale des arbres
N_SONDES = 3  # par arbre

# Position des murs
ANGLES = [[9, 5], [942, 1], [986, 312], [542, 396], [18, 250]]
MURS = [[a, ANGLES[i + 1] if i + 1 < len(ANGLES) else ANGLES[0]] for i, a in enumerate(ANGLES)]

Hote = IntEnum('Hôte', 'jiro moro ame yuki')
try:
    CURRENT_HOST = Hote[gethostname().split('.')[0].lower()]
except KeyError:
    CURRENT_HOST = Hote.jiro
MAIN_HOST = Hote.jiro
