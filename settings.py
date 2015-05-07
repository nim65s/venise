# -*- coding: utf-8 -*-
from datetime import datetime
from enum import IntEnum
from math import pi
from socket import gethostname

from numpy import array

Hote = IntEnum('Hôte', 'cerf moro ame yuki')
try:
    CURRENT_HOST = Hote[gethostname().split('.')[0].lower()]
except KeyError:
    CURRENT_HOST = Hote.cerf
MAIN_HOST = Hote.cerf
FAILS = []

# Constantes AGV
RAYON_AGV = 1.180
POS_ROUES = [-pi / 4, pi / 4, pi]

# Constantes Tourelles
VIT_MOY_MAX = 16.5  # mm / s
VIT_LIM_REV = 8

DIST_MIN_AGV = 5

# δt
PERIODE = 0.1

# TCP AGV
HOST_AGV = '192.168.1.10'
PORT_AGV = 8001
PORT_UBISENS = 1336
PORT_PUSH = 1337
PORT_PUB = 1338
PORT_CACHE = 1339
PORT_TIM = 2112  # TODO: y’en aura deux sur les AGV, et pour les tests y’a un HOST différent…

N_SONDES = 3  # par arbre

# On veut faire faire pi/2 en 10 cm, si on est à vitesse max
SMOOTH_FACTOR = pi / 2 / (60 * 0.5 / PERIODE)
SMOOTH_SPEED = {
        'v': 0.003 / PERIODE,
        'w': 0.00001 / PERIODE,
        't': 0.003 / PERIODE,
        }


[[-5, -15], [4, 14]]
[[-7, -13], [6, 12]]
_N = 24
ALLER_RETOURS = {
        Hote.moro: [[-12, 7], [-8, 11]],
        Hote.yuki: [[11, 10], [19, 10]],
        Hote.ame: [[13, 14], [18, 14]],
        }
PATHS = {
        Hote.moro: [[-8, 7], [-11, 7], [-11, 10], [-10, 11], [-8, 11]],
        Hote.ame: [[11, 11], [19, 11], [24, 9.5], [25, 7.5], [24, 4.5], [20, 4.5], [15, 7.5], [12, 7.5], [10, 9]],
        Hote.yuki: [[11, 11], [19, 11], [24, 9.5], [25, 7.5], [24, 4.5], [20, 4.5], [15, 7.5], [12, 7.5], [10, 9]],
        #Hote.yuki: [[8, 7], [8, 8], [11, 10], [19, 10], [32, 15], [33, 14], [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [10, 6.5], [9, 6.5]],
        }

BORDS = {
        Hote.moro: [[-7, 6], [-7, 12], [-9, 12], [-13, 8], [-13, 6]],
        Hote.ame: [[8, 7], [8, 8], [11, 14], [13, 17], [14.5, 17.5], [16, 17], [17, 16], [20, 14], [27, 14], [30, 16], [31, 17],
            [33, 17], [34, 16], [34, 15], [32, 13], [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [10, 6.5], [9, 6.5]],
        Hote.yuki: [[8, 7], [8, 8], [11, 14], [13, 17], [14.5, 17.5], [16, 17], [17, 16], [20, 14], [27, 14], [30, 16], [31, 17],
            [33, 17], [34, 16], [34, 15], [32, 13], [24, 9], [25, 7], [25, 4], [20, 4], [15, 7], [12, 7], [10, 6.5], [9, 6.5]],
        }

# SVG
WIDTH = 35 + 15
HEIGHT = 20
PX_PAR_M = 35
PATHS_SVG = {h: array(PATHS[h]) * PX_PAR_M for h in [2, 3, 4]}
ALLER_RETOURS_SVG = {h: array(ALLER_RETOURS[h]) * PX_PAR_M for h in [2, 3, 4]}
BORDS_SVG = {h: array(BORDS[h]) * PX_PAR_M for h in [2, 3, 4]}

BERCAIL = {
        Hote.moro: (-10, 9),
        Hote.yuki: (8, 6),
        Hote.ame: (9, 11),
        }

DATA = {
        'status': 'Pas connecté',
        'x': 0, 'y': 0, 'a': 0,  # Position
        'v': 0, 'w': 0, 't': 0,  # Vitesse
        'vg': 0, 'wg': 0, 'tg': 0,  # Vitesse
        'vt': [0, 0, 0], 'vc': [0, 0, 0], 'tt': [0, 0, 0], 'tm': [0, 0, 0], 'tc': [0, 0, 0], 'nt': [0, 0, 0],  # Tourelles vitesse, target, mesuree, consigne, nombre de tours, nombre de tours
        'granier': [0] * N_SONDES, 'gmi': [10] * N_SONDES, 'gma': [-10] * N_SONDES, 'gm': [0] * N_SONDES,  # Sondes granier
        'start': True, 'smoothe': True, 'smoothe_speed': True, 'boost': False, 'arriere': False, 'reverse': True, 'sens': True,  # Boutons
        'reversed': [False, False, False], 'last_seen_agv': str(datetime(1970, 1, 1)),  'destination': [[0, 0], [0, 0], [0, 0]], 'state': -1,  # Détails d’implémentation…
        }

