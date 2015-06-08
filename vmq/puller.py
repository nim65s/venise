from argparse import ArgumentParser
from datetime import datetime

from zmq import NOBLOCK, PULL
from zmq.error import Again

from ..settings import PORT_PUSH
from .vmq import VMQ, vmq_parser


class Puller(VMQ):
    def __init__(self, wait=True, port_push=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.puller = self.context.socket(PULL)
        url = "tcp://*:%i" % (PORT_PUSH + port_push * 10 * self.hote)
        self.printe(url)
        self.puller.bind(url)
        self.last_seen = datetime(1970, 1, 1)
        if wait:
            print('Attente de connexion')
            self.pull(block=0)
            print('Connecté')

    def pull(self, block=NOBLOCK):
        while True:
            try:
                num, data = self.puller.recv_json(block)
                if num in self.hotes:
                    self.data[num].update(**data)
                    self.last_seen = datetime.now()
            except Again:
                break
            if block != NOBLOCK:
                break

puller_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
puller_parser.add_argument('--port_push', action='store_true')
