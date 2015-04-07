from argparse import ArgumentParser
from math import atan2, cos, hypot, pi, sin
from time import sleep

from ..settings import Hote, PERIODE, POS_ROUES, VIT_MOY_MAX
from ..vmq.puller_publisher import PullerPublisher


class Trajectoire(PullerPublisher):
    def __init__(self, period, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.data = {h: {
            'stop': False,
            'hote': h,
            'x': 0, 'y': 0, 'a': 0,  # Position
            'v': 0, 'w': 0, 't': 0,  # Vitesse
            't1': 0, 'v1': 0, 't2': 0, 'v2': 0, 't3': 0, 'v3': 0,  # Tourelles
            'granier': [], 'sick': [], 'luminosite': [],  # Sondes
            } for h in Hote}

    def loop(self):
        try:
            while self.period:
                self.pull()
                self.update()
                self.pub()
                sleep(self.period)
        except KeyboardInterrupt:
            self.stop()

    def stop(self, hotes=Hote):
        if isinstance(hotes, Hote):
            hotes = [hotes]
        print('stopping %s…' % ', '.join([h.name for h in hotes]))
        for hote in hotes:
            self.data[hote].update(t1=0, v1=VIT_MOY_MAX, t2=0, v2=VIT_MOY_MAX, t3=0, v3=VIT_MOY_MAX)
        self.pub()
        sleep(6)
        for hote in hotes:
            self.data[hote].update(t1=0, v1=0, t2=0, v2=0, t3=0, v3=0)
        self.pub()
        sleep(1)
        for hote in hotes:
            self.data[hote].update(stop=True)
        self.pub()
        print('stopped.')

    def update(self):
        for hote in Hote:
            self.data[hote].update(**self.process_speed(**self.data[hote]))
            self.data[hote].update(**self.process_tourelles(**self.data[hote]))

    def process_speed(self, **kwargs):
        raise NotImplementedError()

    def tourelle(self, pos_roue, v, w, t, **kwargs):
        vit_x = v * cos(t) - w * sin(pos_roue)
        vit_y = v * sin(t) + w * cos(pos_roue)
        return atan2(vit_y, vit_x) % (2 * pi), VIT_MOY_MAX * hypot(vit_x, vit_y)

    def process_tourelles(self, **kwargs):
        (t1, v1), (t2, v2), (t3, v3) = [self.tourelle(POS_ROUES[i], **kwargs) for i in range(3)]
        return {'t1': t1, 'v1': v1, 't2': t2, 'v2': v2, 't3': t3, 'v3': v3}


trajectoire_parser = ArgumentParser()
trajectoire_parser.add_argument('-T', '--period', type=float, default=PERIODE, help="période d’envoie des données aux sorties")
