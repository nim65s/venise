#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division, absolute_import

from math import pi, sin, cos, atan2, hypot
from random import random
import socket
from time import sleep

from .utils import BoundedVar, CheckedVar
from ..settings import MAX_X, MAX_Y, POS_ROUES, VIT_ANG_MAX, VIT_LIN_MAX, ACC_LIN_MAX, PERIODE, HOST, PORT


class ArbreAGV(object):
    # position
    x = BoundedVar('x', MAX_X, 0)
    y = BoundedVar('y', MAX_Y, 0)
    a = BoundedVar('α', pi, circular=True)
    # vitesse
    v = BoundedVar('v', 1)
    w = BoundedVar('ω', 1)
    t = BoundedVar('θ', pi, circular=True)
    # consignes des tourelles
    t1 = CheckedVar('t1', VIT_ANG_MAX * PERIODE, max=2 * pi, min=0, circular=True)
    v1 = CheckedVar('v1', ACC_LIN_MAX * PERIODE, VIT_LIN_MAX)
    t2 = CheckedVar('t2', VIT_ANG_MAX * PERIODE, max=2 * pi, min=0, circular=True)
    v2 = CheckedVar('v2', ACC_LIN_MAX * PERIODE, VIT_LIN_MAX)
    t3 = CheckedVar('t3', VIT_ANG_MAX * PERIODE, max=2 * pi, min=0, circular=True)
    v3 = CheckedVar('v3', ACC_LIN_MAX * PERIODE, VIT_LIN_MAX)

    def update_pos(self):
        " Incrémente la position depuis la vitesse "
        self.x += self.v * cos(self.t)
        self.y += self.v * sin(self.t)
        self.a += self.w
        return (self.x, self.y, self.a)

    def update_vit(self, v=None, w=None, t=None):
        " Met à jour la vitesse, aléatoirement si nécessaire "
        if v is None and w is None and t is None:
            self.v += (random() - 0.5) / 500000000
            self.w += (random() - 0.5) / 500000000
            self.t += (random() - 0.5) / 500000000 * pi
        else:
            self.v, self.w, self.t, = v, w, t
        return (self.v, self.w, self.t)

    def roue(self, i):
        " Génère la consigne en angle et vitesse de rotation pour la tourelle i "
        vit_x = self.v * cos(self.t) - self.w * sin(POS_ROUES[i])
        vit_y = self.v * sin(self.t) + self.w * cos(POS_ROUES[i])
        return atan2(vit_y, vit_x), VIT_LIN_MAX * hypot(vit_x, vit_y) / 2

    def roues(self):
        " Met à jour les consignes pour les tourelles "
        (self.t1, self.v1), (self.t2, self.v2), (self.t3, self.v3) = [self.roue(i) for i in range(3)]

    def send(self):
        " Génère les commandes à envoyer à l’API de l’AGV "
        return u'setSpeedAndPosition({t1}, {v1}, {t2}, {v2}, {t3}, {v3})'.format(**self.__dict__)

    def maxima(self):
        " Affiche les maxima atteints par toutes les variables… En attendant de meilleurs logs "
        for i in ['x', 'y', 'a', 'v', 'w', 't', 't1', 'v1', 't2', 'v2', 't3', 'v3']:
            print('%s: %.3f (%.3f ~ %.3f)' % (i, self.__dict__[i], self.__dict__[i + '_min'], self.__dict__[i + '_max']))


def run():
    a = ArbreAGV()
    s = socket.socket()
    print 'connecting...'
    s.connect((HOST, PORT))
    print 'connected'
    try:
        while True:
            a.update_pos()
            a.update_vit()
            a.roues()
            if s is not None and False:
                s.sendall(a.send())
                ret = s.recv(1024)
                if ret.startswith('+'):  # Les erreurs commencent par un +
                    print ret
                    break
            else:
                print a.send()
            sleep(PERIODE)
    except KeyboardInterrupt:
        print
        a.maxima()


if __name__ == '__main__':
    run()
