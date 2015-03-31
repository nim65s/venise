from math import atan2, copysign, cos, hypot, pi, sin
from pprint import pprint
from time import sleep, time

from zmq import Context, NOBLOCK, PUB, PULL
from zmq.error import Again

from .settings import ACC_LIN_MAX, ENTREES_PORT, hosts, PERIODE, POS_ROUES, SORTIES_PORT, VIT_ANG_MAX, VIT_MOY_MAX


class Trajectoire(object):
    def __init__(self, period=PERIODE):
        self.period = period
        self.context = Context()

        self.publisher = self.context.socket(PUB)
        self.publisher.bind("tcp://*:%i" % SORTIES_PORT)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % ENTREES_PORT)

        self.data = {i: {
            'stop': False,
            'x': 0, 'y': 0, 'a': 0,  # Position
            'v': 0, 'w': 0, 't': 0,  # Vitesse
            't1': 0, 'v1': 0, 't2': 0, 'v2': 0, 't3': 0, 'v3': 0,  # Tourelles
            } for i in hosts}

    def pull(self):
        while True:
            try:
                num, vals = self.puller.recv_json(NOBLOCK)
                self.data[num].update(**vals)
            except Again:
                break

    def pub(self):
        self.publisher.send_json(self.data)

    def loop(self):
        try:
            while self.period:
                self.pull()
                #self.update()
                self.pub()
                sleep(self.period)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print('stopping…')
        for host in hosts:
            self.data[host].update(t1=0, v1=VIT_MOY_MAX, t2=0, v2=VIT_MOY_MAX, t3=0, v3=VIT_MOY_MAX)
        self.pub()
        sleep(3)
        for host in hosts:
            self.data[host].update(t1=0, v1=0, t2=0, v2=0, t3=0, v3=0)
        self.pub()
        sleep(1)
        for host in hosts:
            self.data[host].update(stop=True)
        self.pub()
        print('stopped.')

    def update(self):
        for host in hosts:
            self.data[host].update(**self.process_speed(host, **self.data[host]))
            self.data[host].update(**self.process_tourelles(host, **self.data[host]))

    def process_speed(self, host, **kwargs):
        raise NotImplementedError()

    def tourelle(self, roue, v, t, w, **kwargs):
        vit_x = v * cos(t) - w * sin(roue)
        vit_y = v * sin(t) + w * cos(roue)
        return atan2(vit_y, vit_x) % (2 * pi), VIT_MOY_MAX * hypot(vit_x, vit_y)

    def process_tourelles(self, host, **kwargs):
        (t1, v1), (t2, v2), (t3, v3) = [self.tourelle(POS_ROUES[i], **self.data[host]) for i in range(3)]
        return {'t1': t1, 'v1': v1, 't2': t2, 'v2': v2, 't3': t3, 'v3': v3}
