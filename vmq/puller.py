from datetime import datetime

from zmq import NOBLOCK, PULL
from zmq.error import Again

from ..settings import PORT_PUSH
from .vmq import VMQ


class Puller(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % PORT_PUSH)
        self.last_seen = datetime(1970, 1, 1)
        self.pull(block=0)

    def pull(self, block=NOBLOCK):
        while True:
            try:
                num, data = self.puller.recv_json(block)
                self.data[num].update(**data)
                self.last_seen = datetime.now()
                self.printe(data)
            except Again:
                break
            if block != NOBLOCK:
                break
