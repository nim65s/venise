from argparse import ArgumentParser
from datetime import datetime
from math import atan2, copysign, cos, hypot, pi, sin
from time import sleep

from numpy import array

from ..settings import BOUNDARIES, DATA, PERIOD, WHEEL_POS, SMOOTH_SPEED, SPEED_MEAN_MAX
from ..utils.dist_angles import dist_angle
from ..utils.point_in_polygon import wn_pn_poly
from ..vmq import Publisher, Puller, vmq_parser


class Trajectory(Puller, Publisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(wait=False, *args, **kwargs)
        self.period = period
        self.data = {h: DATA.copy() for h in self.hosts}
        for h in self.hosts:
            self.data[h]['host'] = h
        self.data['trajectory'] = self.__class__.__name__

    def send(self):
        self.pub()

    def loop(self):
        self.pull()
        self.update()
        self.send()
        sleep(self.period)

    def end(self):
        return

    def update(self):
        for host in self.hosts:
            self.data[host].update(**self.inside(**self.data[host]))
            self.data[host].update(**self.process_speed(**self.data[host]))
            self.data[host].update(**self.smooth_speed(**self.data[host]))
            self.data[host].update(**self.process_turrets(**self.data[host]))

    def process_speed(self, **kwargs):
        raise NotImplementedError()

    def smooth_speed(self, smoothe_speed, v, w, t, vg, wg, tg, **kwargs):
        if smoothe_speed:
            dv, dw, dt = v - vg, w - wg, dist_angle(t, tg)
            return {
                'v': round(v - copysign(SMOOTH_SPEED['v'], dv), 5) if abs(dv) > SMOOTH_SPEED['v'] else vg,
                'w': round(w - copysign(SMOOTH_SPEED['w'], dw), 5) if abs(dw) > SMOOTH_SPEED['w'] else wg,
                't': round((t - copysign(SMOOTH_SPEED['t'], dt)) % (2 * pi), 5) if abs(dt) > SMOOTH_SPEED['t'] else tg,
            }
        return {'v': vg, 'w': wg, 't': tg}

    def turret(self, wheel_pos, v, w, t, **kwargs):
        vit_x = v * cos(t) - w * sin(wheel_pos)
        vit_y = v * sin(t) + w * cos(wheel_pos)
        return round(atan2(vit_y, vit_x) % (2 * pi), 5), round(SPEED_MEAN_MAX * hypot(vit_x, vit_y), 5)

    def process_turrets(self, **kwargs):
        tt, vt = zip(*[self.turret(WHEEL_POS[i], **kwargs) for i in range(3)])
        vt = array(vt)
        return {'tt': tt, 'vt': (vt * 2 * SPEED_MEAN_MAX / abs(vt).max()).tolist() if abs(vt).max() != 0 else [0, 0, 0]}

    def inside(self, host, x, y, **kwargs):
        return {'inside': wn_pn_poly((x, y), BOUNDARIES[host]) != 0}


trajectory_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
trajectory_parser.add_argument('-T', '--period', type=float, default=PERIOD, help="main loop period")
