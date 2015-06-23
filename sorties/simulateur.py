from datetime import datetime
from time import sleep

from numpy import array, cos, cross, dot, pi, sin, where

from ..settings import PERIODE, POS_ROUES, RAYON_AGV, SMOOTH_FACTOR
from ..utils.dist_angles import dist_angles
from ..vmq import puller_parser
from .sortie import Sortie

now = datetime.now
A, B, C = X, Y, Z = range(3)


class Simulateur(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_send = ['vc', 'tc', 'vm', 'tm', 'nt', 'reversed', 'x', 'y', 'a']
        self.data[self.hote]['reversed'] = [False, False, False]

    def loop(self):
        self.pull()
        self.process(**self.data[self.hote])
        for var in self.to_send:
            self.push.send_json([self.hote, {var: array(self.data[self.hote][var]).round(5).tolist()}])
        self.push.send_json([self.hote, {'last_seen_agv': str(now()), 'status': 'Simulateur', 'erreurs': 'ok'}])
        sleep(PERIODE)

    def process(self, reverse, smoothe, hote, boost, arriere, stop, **kwargs):
        self.data[hote].update(**self.copy_consignes(**self.data[hote]))
        if reverse:
            self.data[hote].update(**self.reverse(**self.data[hote]))
        if smoothe:
            self.data[hote].update(**self.smoothe(**self.data[hote]))
        if boost:
            self.data[hote].update(**self.boost(**self.data[hote]))
        if arriere:
            self.data[hote].update(**self.arriere(**self.data[hote]))
        if stop:
            self.data[hote].update(vc=array([0, 0, 0]))
        self.data[hote].update(**self.recv_agv(**self.data[hote]))
        self.data[hote].update(**self.tourelles_to_movement(**self.data[hote]))

    def recv_agv(self, vc, tc, nt, **kwargs):
        return {'vm': vc * 0.5, 'tm': tc, 'nt': nt}

    def copy_consignes(self, vt, tt, reversed, **kwargs):
        return {'vc': array(vt), 'tc': array(tt), 'reversed': array(reversed)}

    def reverse(self, vc, tc, tm, reversed, **kwargs):
        vc[where(reversed)] *= -1
        tc[where(reversed)] += pi
        tc[where(reversed)] %= 2 * pi
        rev = abs(dist_angles(tm, tc)) > 2 * pi / 3
        vc[where(rev)] *= -1
        tc[where(rev)] += pi
        tc[where(rev)] %= 2 * pi
        reversed ^= rev
        return {'vc': vc, 'reversed': reversed}

    def smoothe(self, tm, tc, hote, **kwargs):
        dst = dist_angles(tm, tc)
        return {'tc': tc if abs(dst).max() < SMOOTH_FACTOR[hote] else (tm - SMOOTH_FACTOR[hote] * dst / abs(dst).max()) % (2 * pi)}

    def boost(self, tg, **kwargs):
        return {'vc': array([80, 80, 80]), 'tc': array([tg, tg, tg])}

    def arriere(self, vc, **kwargs):
        return {'vc': -vc}

    def tourelles_to_movement(self, vm, tm, x, y, a, **kwargs):
        v_r = (vm * array([cos(tm), sin(tm), [0, 0, 0]])).transpose()
        p_r = RAYON_AGV * 1000 * array([cos(POS_ROUES), sin(POS_ROUES), [0, 0, 0]]).transpose()
        w = array([0, 0, (v_r[C][Y] - v_r[A][Y]) / (p_r[C][X] - p_r[A][X])])
        v_o = dot(self.rot(a), (v_r[A] + cross(w, -p_r[A]))[:2])
        x -= v_o[X] / 1000
        y -= v_o[Y] / 1000
        a += w[Z]
        return {'x': x, 'y': y, 'a': a}

    def rot(self, a):
        return array([[cos(a), -sin(a)], [sin(a), cos(a)]])


if __name__ == '__main__':
    puller_parser.set_defaults(port_push=True)
    Simulateur(**vars(puller_parser.parse_args())).run()
