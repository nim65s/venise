from zmq import PUSH
from argparse import ArgumentParser
from datetime import datetime
from math import atan2, cos, hypot, pi, sin
from time import sleep

from ..settings import PERIODE, POS_ROUES, VIT_MOY_MAX, PORT_PUSH, N_SONDES, DATA
from ..vmq import Puller, Publisher, vmq_parser


class Trajectoire(Puller, Publisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(wait=False, *args, **kwargs)
        self.period = period
        self.data = {h: DATA.copy() for h in self.hotes}
        for h in self.hotes:
            self.data[h]['hote'] = h
        self.data['timestamp'] = datetime.now().timestamp()
        self.data['trajectoire'] = self.__class__.__name__

        self.push = {h: self.context.socket(PUSH) for h in self.hotes}
        for h in self.hotes:
            self.push[h].connect('tcp://%s:%i' % (h.name, PORT_PUSH))

    def send(self):
        self.data['timestamp'] = datetime.now().timestamp()
        self.pub()
        for h in self.hotes:
            self.push[h].send_json([h, self.data[h]])

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
            self.data[hote].update(**self.process_tourelles(**self.data[hote]))
        self.data['timestamp'] = datetime.now().timestamp()

    def process_speed(self, **kwargs):
        raise NotImplementedError()

    def tourelle(self, pos_roue, v, w, t, **kwargs):
        vit_x = v * cos(t) - w * sin(pos_roue)
        vit_y = v * sin(t) + w * cos(pos_roue)
        return round(atan2(vit_y, vit_x) % (2 * pi), 5), round(VIT_MOY_MAX * hypot(vit_x, vit_y), 5)

    def process_tourelles(self, **kwargs):
        tt, vt = zip(*[self.tourelle(POS_ROUES[i], **kwargs) for i in range(3)])
        if sum(abs(v) < 5 for v in vt > 1:
            vt = [0, 0, 0]
        return {'tt': tt, 'vt': vt}


trajectoire_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
trajectoire_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données aux sorties")
