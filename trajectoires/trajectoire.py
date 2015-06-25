from argparse import ArgumentParser
from datetime import datetime
from math import atan2, copysign, cos, hypot, pi, sin
from os.path import expanduser, isfile
from time import sleep

from numpy import array

from ..settings import DATA, PERIODE, POS_ROUES, SMOOTH_SPEED, VIT_MOY_MAX
from ..utils.dist_angles import dist_angle
from ..vmq import Publisher, Puller, vmq_parser


class Trajectoire(Puller, Publisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(wait=False, *args, **kwargs)
        self.period = period
        self.data = {h: DATA.copy() for h in self.hotes}
        for h in self.hotes:
            self.data[h]['hote'] = h
        self.data['timestamp'] = datetime.now().timestamp()
        self.data['trajectoire'] = self.__class__.__name__

    def send(self):
        self.data['timestamp'] = datetime.now().timestamp()
        self.pub()

    def loop(self):
        self.pull()
        self.update()
        self.send()
        sleep(self.period)

    def fin(self):
        return
        print('stopping %s…' % ', '.join([h.name for h in self.hotes]))
        for hote in self.hotes:
            self.data[hote].update(v=1, w=0, t=0, t1=0, v1=VIT_MOY_MAX, t2=0, v2=VIT_MOY_MAX, t3=0, v3=VIT_MOY_MAX)
        self.send()
        sleep(6)
        for hote in self.hotes:
            self.data[hote].update(v=0, v1=0, v2=0, v3=0)
        self.send()
        sleep(1)
        for hote in self.hotes:
            self.data[hote].update(stop=True)
        self.send()
        print('stopped.')
        super().fin()

    def update(self):
        for hote in self.hotes:
            self.data[hote].update(**self.process_speed(**self.data[hote]))
            self.data[hote].update(**self.smooth_speed(**self.data[hote]))
            self.save_speed(**self.data[hote])
            self.data[hote].update(**self.process_tourelles(**self.data[hote]))
        self.data['timestamp'] = datetime.now().timestamp()

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

    def tourelle(self, pos_roue, v, w, t, **kwargs):
        vit_x = v * cos(t) - w * sin(pos_roue)
        vit_y = v * sin(t) + w * cos(pos_roue)
        return round(atan2(vit_y, vit_x) % (2 * pi), 5), round(VIT_MOY_MAX * hypot(vit_x, vit_y), 5)

    def process_tourelles(self, **kwargs):
        tt, vt = zip(*[self.tourelle(POS_ROUES[i], **kwargs) for i in range(3)])
        vt = array(vt)
        return {'tt': tt, 'vt': (vt * 2 * VIT_MOY_MAX / abs(vt).max()).tolist()}

    def save_speed(self, hote, v, w, t, **kwargs):
        with open(expanduser('~/.state_speed_%i' % hote), 'w') as f:
            print([v, w, t], file=f)

    def get_speed(self, hote):
        filename = expanduser('~/.state_speed_%i' % hote)
        if isfile(filename):
            with open(filename, 'r') as f:
                v, w, t = eval(f.read())
        else:
            v, w, t = 0, 0, 0
        return {'v': v, 'w': w, 't': t}


trajectoire_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
trajectoire_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données aux sorties")
