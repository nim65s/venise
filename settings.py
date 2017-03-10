# -*- coding: utf-8 -*-
from datetime import datetime
from enum import IntEnum
from math import pi, sqrt
from socket import gethostname

from numpy import array

PROD = gethostname() in ['cerf', 'moro', 'ame', 'yuki']

Hote = IntEnum('Hôte', 'cerf moro ame yuki nausicaa')
try:
    CURRENT_HOST = Hote[gethostname().split('.')[0].lower()]
except KeyError:
    CURRENT_HOST = Hote.cerf if PROD else Hote.nausicaa
MAIN_HOST = Hote.cerf if PROD else Hote.nausicaa

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
SMOOTH_FACTOR = {
        Hote.moro: pi / 2 / (60 * 0.2 / PERIODE),
        Hote.ame: pi / 2 / (60 * 0.1 / PERIODE),
        Hote.yuki: pi / 2 / (60 * 0.1 / PERIODE),
        }

SMOOTH_SPEED = {
        'v': 0.003 / PERIODE,
        'w': 0.00001 / PERIODE,
        't': 0.003 / PERIODE,
        }


ALLER_RETOURS = {
        Hote.moro: [[-12, 7], [-8, 11]],
        Hote.yuki: [[11, 10], [19, 10]],
        Hote.ame: [[13, 14], [18, 14]],
        }
_PATHS = {h: [[[1.5, 6.5], [4, 7], [1.5, 8], [3, 10],[1.5,12],[3.5,13]]] for h in [Hote.moro, Hote.ame, Hote.yuki]}


def echelonne_path(dep, ari):
    dep, ari = array(dep), array(ari)
    d = sqrt(sum((dep - ari) ** 2))
    return [(dep + i * (ari - dep) / d).round(2).tolist() for i in range(int(d))]

PATHS = {h: [sum([echelonne_path(p[i], p[(i + 1) % len(p)])
    for i in range(len(p))], []) for p in _PATHS[h]] for h in [Hote.moro, Hote.ame, Hote.yuki]}


BORDS = {h: [[1, 6], [.8, 12.5], [4.7, 14], [3.65, 11.8],[3,9.75],[3.8,7.4],[4.6,6.4]] for h in [Hote.moro, Hote.ame, Hote.yuki]}

# SVG
WIDTH = 7
HEIGHT = 10
PX_PAR_M = 35
PATHS_SVG = {h: [array(p) * PX_PAR_M for p in _PATHS[h]] for h in [2, 3, 4]}
ALLER_RETOURS_SVG = {h: array(ALLER_RETOURS[h]) * PX_PAR_M for h in [2, 3, 4]}
BORDS_SVG = {h: array(BORDS[h]) * PX_PAR_M for h in [2, 3, 4]}

BERCAIL = {
        Hote.moro: (-10, 9),
        Hote.ame: (6.5, 6),
        Hote.yuki: (7, 11),
        }
MORNING = {
        Hote.moro: (-8, 7),
        Hote.ame: (12, 7.5),
        Hote.yuki: (23, 9.5),
        }

DATA = {
        'status': 'Pas connecté', 'erreurs': 'Pas connecté', 'anomaly': False, 'is_up': False,
        'x': 0, 'y': 0, 'a': 0,  # Position
        'v': 0, 'w': 0, 't': 0,  # Vitesse
        'vg': 0, 'wg': 0, 'tg': 0,  # Vitesse
        'vt': [0, 0, 0], 'vm': [0, 0, 0], 'vc': [0, 0, 0], 'tt': [0, 0, 0], 'tm': [0, 0, 0], 'tc': [0, 0, 0], 'nt': [0, 0, 0],
        # Tourelles vitesse, target, mesuree, consigne, nombre de tours, nombre de tours
        'granier': [0] * N_SONDES, 'gmi': [10] * N_SONDES, 'gma': [-10] * N_SONDES, 'gm': [0] * N_SONDES,  # Sondes granier
        'stop': False, 'smoothe': True, 'smoothe_speed': True, 'boost': False, 'arriere': False, 'reverse': True,
        'sens': bool((datetime.now()).day % 2), 'dest_next': False, 'dest_prev': False, 'path_next': False, 'path_prev': False, 'rotation': True,  # Boutons
        'reversed': [False, False, False], 'last_seen_agv': str(datetime(1970, 1, 1)), 'destination': [0, 0], 'state': -1, 'choosen_path': -1,
        }

Phase = IntEnum('Phase', 'parking sort_yuki sort_ame tourne rentre_ame rentre_yuki auto')

GRID_COEF = 4
