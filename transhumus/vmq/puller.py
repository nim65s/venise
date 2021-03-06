from datetime import datetime

from zmq import NOBLOCK, PULL
from zmq.error import Again

from ..settings import PORT_PUSH
from .vmq import VMQ


class Puller(VMQ):
    def __init__(self, wait=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % PORT_PUSH)

        self.last_seen = datetime(1970, 1, 1)
        if wait:
            print('Waiting for a connexion')
            self.pull(block=0)
            print('Connected')

    def pull(self, block=NOBLOCK):
        while True:
            try:
                num, data = self.puller.recv_json(block)
                if num in self.hosts:
                    self.data[num].update(**data)
                    self.last_seen = datetime.now()
            except Again:
                break
            if block != NOBLOCK:
                break
