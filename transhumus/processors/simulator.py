from datetime import datetime
from math import tau

from numpy import array, cos, cross, dot, pi, sin, where

from ..settings import WHEEL_POS, AGV_RADIUS, SMOOTH_FACTOR
from ..utils.dist_angles import dist_angles
from .processor import Processor, processor_parser

now = datetime.now
A, B, C = X, Y, Z = range(3)


class Simulator(Processor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data[self.host]['reversed'] = [False, False, False]
        self.to_send = ['vc', 'tc', 'vm', 'tm', 'nt', 'reversed', 'x', 'y', 'a']

    def process(self, reverse, smoothe, host, boost, back, stop, **kwargs):
        self.data[host].update(**self.copy_orders(**self.data[host]))
        if reverse:
            self.data[host].update(**self.reverse(**self.data[host]))
        if smoothe:
            self.data[host].update(**self.smoothe(**self.data[host]))
        if boost:
            self.data[host].update(**self.boost(**self.data[host]))
        if back:
            self.data[host].update(**self.back(**self.data[host]))
        if stop:
            self.data[host].update(vc=array([0, 0, 0]))
        self.data[host].update(**self.recv_agv(**self.data[host]))
        self.data[host].update(**self.turrets_to_movement(**self.data[host]))
        self.data[host].update(**self.to_list(**self.data[host]))
        self.data[host].update(**self.round(**self.data[host]))
        return {var: self.data[host][var] for var in self.to_send}

    def round(self, **kwargs):
        return {var: [round(i, 5) for i in kwargs[var]] for var in ['tc', 'tm', 'vc', 'vm']}

    def to_list(self, **kwargs):
        return {var: kwargs[var].tolist() for var in ['tc', 'vc', 'vm', 'tm', 'reversed']}

    def recv_agv(self, vc, tc, nt, **kwargs):
        return {'vm': vc * 0.5, 'tm': tc, 'nt': nt}

    def copy_orders(self, vt, tt, reversed, **kwargs):
        return {'vc': array(vt), 'tc': array(tt), 'reversed': array(reversed)}

    def reverse(self, vc, tc, tm, reversed, **kwargs):
        vc[where(reversed)] *= -1
        tc[where(reversed)] += pi
        tc[where(reversed)] %= tau
        rev = abs(dist_angles(tm, tc)) > tau / 3
        vc[where(rev)] *= -1
        tc[where(rev)] += pi
        tc[where(rev)] %= tau
        reversed ^= rev
        return {'vc': vc, 'reversed': reversed}

    def smoothe(self, tm, tc, host, **kwargs):
        dst = dist_angles(tm, tc)
        tc = tc if abs(dst).max() < SMOOTH_FACTOR[host] else (tm - SMOOTH_FACTOR[host] * dst / abs(dst).max()) % tau
        return {'tc': tc}

    def boost(self, tg, **kwargs):
        return {'vc': array([80, 80, 80]), 'tc': array([tg, tg, tg])}

    def back(self, vc, **kwargs):
        return {'vc': -vc}

    def turrets_to_movement(self, vm, tm, x, y, a, **kwargs):
        v_r = (vm * array([cos(tm), sin(tm), [0, 0, 0]])).transpose()
        p_r = AGV_RADIUS * 1000 * array([cos(WHEEL_POS), sin(WHEEL_POS), [0, 0, 0]]).transpose()
        w = array([0, 0, (v_r[C][Y] - v_r[A][Y]) / (p_r[C][X] - p_r[A][X])])
        v_o = dot(self.rot(a), (v_r[A] + cross(w, -p_r[A]))[:2])
        x -= v_o[X] / 1000
        y -= v_o[Y] / 1000
        a += w[Z]
        return {'x': x, 'y': y, 'a': a}

    def rot(self, a):
        return array([[cos(a), -sin(a)], [sin(a), cos(a)]])


if __name__ == '__main__':
    Simulator(**vars(processor_parser.parse_args())).run()
