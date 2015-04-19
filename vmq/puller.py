from zmq import NOBLOCK, PULL
from zmq.error import Again

from ..settings import PORT_ENTREES
from .vmq import VMQ


class Puller(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % PORT_ENTREES)

    def pull(self):
        while True:
            try:
                num, data = self.puller.recv_json(NOBLOCK)
                self.data[num].update(**data)
                if self.verbosite > 2:
                    self.printe(data)
            except Again:
                break
