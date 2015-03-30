from math import atan2, copysign, cos, hypot, sin
from time import sleep

from zmq import Context, NOBLOCK, PUB, PULL
from zmq.error import Again

from .settings import ACC_LIN_MAX, ENTREES_PORT, hosts, PERIODE, POS_ROUES, SORTIES_PORT, VIT_ANG_MAX, VIT_LIN_MAX


class Trajectoire(object):
    def __init__(self, period=PERIODE):
        self.period = period
        self.context = Context()

        self.publisher = self.context.socket(PUB)
        self.publisher.bind("tcp://*:%i" % SORTIES_PORT)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % ENTREES_PORT)

        self.data = {i: {
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
        while self.period:
            self.pull()
            self.update()
            self.pub()

            sleep(self.period)

    def update(self):
        for host in hosts:
            self.data[host].update(**self.process_speed(host))
            # self.data[host].update(**self.process_pos(host))
            self.data[host].update(**self.process_tourelles(host))

    def process_speed(self, host):
        raise NotImplementedError()

    def process_pos(self, host):
        return {
                'x': self.data[host]['x'] + self.data[host]['v'] * cos(self.data[host]['t']),
                'y': self.data[host]['y'] + self.data[host]['v'] * sin(self.data[host]['t']),
                'a': self.data[host]['a'] + self.data[host]['w'],
                }

    def tourelle(self, host, i):
        vit_x = self.data[host]['v'] * cos(self.data[host]['t']) - self.data[host]['w'] * sin(POS_ROUES[i])
        vit_y = self.data[host]['v'] * sin(self.data[host]['t']) + self.data[host]['w'] * cos(POS_ROUES[i])
        return atan2(vit_y, vit_x), VIT_LIN_MAX * hypot(vit_x, vit_y) / 2

    def process_tourelles(self, host):
        maxi = VIT_ANG_MAX * PERIODE
        (t1, v1), (t2, v2), (t3, v3) = [self.tourelle(host, i) for i in range(3)]
        ok_vit = True
        if abs(t1 - self.data[host]['t1']) > maxi:
            t1 = self.data[host]['t1'] + copysign(maxi, t1 - self.data[host]['t1'])
            ok_vit = False
        if abs(t2 - self.data[host]['t2']) > maxi:
            t2 = self.data[host]['t2'] + copysign(maxi, t2 - self.data[host]['t2'])
            ok_vit = False
        if abs(t3 - self.data[host]['t3']) > maxi:
            t3 = self.data[host]['t3'] + copysign(maxi, t3 - self.data[host]['t3'])
            ok_vit = False
        if not ok_vit:
            print('on tourne')
            v1 = 0
            v2 = 0
            v3 = 0
        return {'t1': t1, 'v1': v1, 't2': t2, 'v2': v2, 't3': t3, 'v3': v3}
