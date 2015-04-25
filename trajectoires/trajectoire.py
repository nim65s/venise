from argparse import ArgumentParser
from datetime import datetime
from math import atan2, cos, hypot, pi, sin
from time import sleep

from ..settings import PERIODE, POS_ROUES, VIT_MOY_MAX
from ..vmq import Publisher, Puller, vmq_parser


class Trajectoire(Puller, Publisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.data = {h: {
            'stop': False,
            'hote': h,
            'event': None,
            'x': 0, 'y': 0, 'a': 0,  # Position
            'v': 0, 'w': 0, 't': 0,  # Vitesse
            't1': 0, 'v1': 0, 't2': 0, 'v2': 0, 't3': 0, 'v3': 0,  # Tourelles
            'granier': [], 'sick': [], 'luminosite': [], 'visiteurs': [],  # Sondes
            } for h in self.hotes}
        self.data['timestamp'] = datetime.now().timestamp()
        self.data['trajectoire'] = self.__class__.__name__

    def loop(self):
        self.pull()
        self.update()
        self.pub()
        sleep(self.period)

    def fin(self):
        print('stopping %s…' % ', '.join([h.name for h in self.hotes]))
        for hote in self.hotes:
            self.data[hote].update(v=1, w=0, t=0, t1=0, v1=VIT_MOY_MAX, t2=0, v2=VIT_MOY_MAX, t3=0, v3=VIT_MOY_MAX)
        self.pub()
        sleep(6)
        for hote in self.hotes:
            self.data[hote].update(v=0, v1=0, v2=0, v3=0)
        self.pub()
        sleep(1)
        for hote in self.hotes:
            self.data[hote].update(stop=True)
        self.pub()
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
        return round(atan2(vit_y, vit_x) % (2 * pi), 4), round(VIT_MOY_MAX * hypot(vit_x, vit_y), 3)

    def process_tourelles(self, **kwargs):
        (t1, v1), (t2, v2), (t3, v3) = [self.tourelle(POS_ROUES[i], **kwargs) for i in range(3)]
        if (abs(v1) < 5) + (abs(v2) < 5) + (abs(v3) < 5) > 1:
            v1 = v2 = v3 = 0
        return {'t1': t1, 'v1': v1, 't2': t2, 'v2': v2, 't3': t3, 'v3': v3}


trajectoire_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
trajectoire_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données aux sorties")
