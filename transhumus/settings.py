import os
from datetime import datetime
from enum import IntEnum
from math import pi, tan
from socket import gethostname

from numpy import array

PROJECT = 'transhumus'
PROJECT_VERBOSE = PROJECT.capitalize()

DOMAIN_NAME = os.environ.get('DOMAIN_NAME', 'localhost')
HOSTNAME = os.environ.get('ALLOWED_HOST', f'{PROJECT}.{DOMAIN_NAME}')
ALLOWED_HOSTS = [HOSTNAME, 'app']
ALLOWED_HOSTS += [f'www.{host}' for host in ALLOWED_HOSTS]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

INSTALLED_APPS = [
    PROJECT,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = f'{PROJECT}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ndh.context_processors.settings_constants',
            ],
        },
    },
]

WSGI_APPLICATION = f'{PROJECT}.wsgi.application'

DB = os.environ.get('DB', 'db.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, DB),
    }
}
if DB == 'postgres':
    DATABASES['default'].update(
        ENGINE='django.db.backends.postgresql',
        NAME=os.environ.get('POSTGRES_DB', DB),
        USER=os.environ.get('POSTGRES_USER', DB),
        HOST=os.environ.get('POSTGRES_HOST', DB),
        PASSWORD=os.environ['POSTGRES_PASSWORD'],
    )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'fr-FR')
TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Paris')
USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = int(os.environ.get('SITE_ID', 1))

MEDIA_ROOT = '/srv/media/'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = '/srv/static/'
LOGIN_REDIRECT_URL = '/'

ASGI_APPLICATION = f"{PROJECT}.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS', 'localhost'), 6379)],
        },
    },
}

NDH_TEMPLATES_SETTINGS = [
    'DATA',
    'CONSTS',
]

# End of Django configuration

# Computers
Host = IntEnum(
    'Host',
    'cerf moro ame yuki nausicaa jiro hattori hagurosan trajectory docker')
try:
    CURRENT_HOST = Host[gethostname().split('.')[0].lower()]
except:
    CURRENT_HOST = Host.docker

MAIN_HOSTS = [host.name for host in Host if not (1 < host < 5)]
MAIN_HOST = CURRENT_HOST if CURRENT_HOST.name in MAIN_HOSTS else Host.cerf

# AGV are more ame and yuki
AGV_HOST = 1 < CURRENT_HOST < 5

# AGV
AGV_RADIUS = 1.180
WHEEL_POS = [-pi / 4, pi / 4, pi]
SPEED_MEAN_MAX = 16.5  # mm / s
SPEED_LIM_REV = 8
DIST_MIN_AGV = 5

# δt
PERIOD = 0.1

# TCP AGV
HOST_AGV = '192.168.1.10'
PORT_AGV = 8001
PORT_UBISENS = 1336
PORT_PUSH = 1337
PORT_PUB = 1338
PORT_CACHE = 1339
PORT_WS = 80

N_PROBES = 3  # for one tree

SMOOTH_FACTOR = {
    Host.ame: pi / 2 / (60 * 0.1 / PERIOD),
}

SMOOTH_SPEED = {
    'v': 0.003 / PERIOD,
    'w': 0.00001 / PERIOD,
    't': 0.003 / PERIOD,
}

BOUNDARIES = {
    Host.ame: [
        [8, 7],
        [8, 8],
        [11, 14],
        [13, 17],
        [14.5, 17.5],
        [16, 17],
        [17, 16],
        [20, 14],
        [27, 14],
        [30, 16],
        [31, 17],
        [33, 17],
        [34, 16],
        [34, 15],
        [32, 13],
        [24, 9],
        [25, 7],
        [25, 4],
        [20, 4],
        [15, 7],
        [12, 7],
        [10, 6.5],
        [9, 6.5],
    ],
}

# SVG
WIDTH = 50
HEIGHT = 20
PX_PER_M = 35
BORDS_SVG = {Host.ame: array(BOUNDARIES[Host.ame]) * PX_PER_M}
_a = 1.15 * PX_PER_M
_b = _a * tan(pi / 8)
OCTOGONE = [(_a, _b), (_b, _a), (-_b, _a), (-_a, _b), (-_a, -_b), (-_b, -_a),
            (_b, -_a), (_a, -_b)]

DATA = {
    'status': 'Not connected',
    'errors': 'Not connected',
    'anomaly': False,
    'is_up': False,
    'inside': False,
    'x': 0,
    'y': 0,
    'a': 0,  # Position
    'v': 0,
    'w': 0,
    't': 0,  # Speed
    'vg': 0,
    'wg': 0,
    'tg': 0,  # Goal Speed
    'vt': [0, 0, 0],
    'tt': [0, 0,
           0],  # target speed and position of turrets computed by trajectory
    'vc': [0, 0, 0],
    'tc': [0, 0, 0],  # orders given to the AGV
    'vm': [0, 0, 0],
    'tm': [0, 0, 0],  # real speed and position of turrets read on AGV
    'nt': [0, 0, 0],  # number of turns by turret
    'granier': [0] * N_PROBES,
    'gmi': [10] * N_PROBES,
    'gma': [-10] * N_PROBES,
    'gm': [0] * N_PROBES,  # Granier probes
    'stop': False,
    'smoothe': False,
    'smoothe_speed': True,
    'boost': False,
    'back': False,
    'reverse': True,
    'reversed': [False, False, False],
    'last_seen_agv': str(datetime(1970, 1, 1)),
    'destination': [0, 0],
    'state': -1,
}

GRID_COEF = 4


def svg_poly(points):
    return ' '.join([','.join(str(n) for n in p) for p in points]),


CONSTS = {
    'px_per_m': PX_PER_M,
    'height': HEIGHT,
    'width': WIDTH,
    'agv_radius': AGV_RADIUS,
    'speed_mean_max': SPEED_MEAN_MAX,
    'octogone': svg_poly(OCTOGONE),
    'bords': svg_poly(BORDS_SVG[3]),
}
