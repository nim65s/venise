from zmq import REQ

from ..settings import PORT_CACHE, MAIN_HOST
from .vmq import VMQ, vmq_parser


class CacheRequester(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requester = self.context.socket(REQ)
        self.requester.connect('tcp://%s:%i' % (MAIN_HOST.name, PORT_CACHE))

    def sub(self):
        self.requester.send_json(self.hote.name)
        data = self.requester.recv_json()
        for h in self.hotes:
            if str(h.value) in data:
                self.data[h].update(**data[str(h.value)])
        self.printe([self.hote, data[str(self.hote.value)] if self.hote > 1 else data])
