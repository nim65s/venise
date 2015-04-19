from zmq import PUB

from ..settings import PORT_SORTIES
from .vmq import VMQ


class Publisher(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.publisher = self.context.socket(PUB)
        self.publisher.bind("tcp://*:%i" % PORT_SORTIES)

    def pub(self):
        self.publisher.send_json(self.data)
        self.printe()
