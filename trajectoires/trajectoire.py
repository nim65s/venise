from time import sleep

from zmq import Context, NOBLOCK, PUB, PULL
from zmq.error import Again

from .settings import ENTREES_PORT, hosts, PERIODE, SORTIES_PORT


class Trajectoire(object):
    def __init__(self, period=PERIODE):
        self.period = period
        self.context = Context()

        self.publisher = self.context.socket(PUB)
        self.publisher.bind("tcp://*:%i" % SORTIES_PORT)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % ENTREES_PORT)

        self.data = {i: {} for i in hosts}

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
            self.data[host].update(**self.process(host))

    def process(self):
        raise NotImplementedError()
