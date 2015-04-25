from zmq import REQ

from ..settings import MAIN_HOST, PORT_CACHE
from .vmq import VMQ


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
