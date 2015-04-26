from datetime import datetime
from zmq import SUB, SUBSCRIBE, NOBLOCK
from zmq.error import Again

from ..settings import MAIN_HOST, PORT_SORTIES
from .vmq import VMQ


class Subscriber(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subscriber = self.context.socket(SUB)
        url = "tcp://%s:%i" % (MAIN_HOST.name, PORT_SORTIES)
        self.printe(url)
        self.subscriber.connect(url)
        self.subscriber.setsockopt_string(SUBSCRIBE, '')  # TODO: les sorties devraient pouvoir override ça
        self.last_seen = datetime(1970, 1, 1)

    def sub(self):
        while True:
            try:
                data = self.subscriber.recv_json(NOBLOCK)
                for h in self.hotes:
                    if str(h.value) in data:
                        self.data[h].update(**data[str(h.value)])
                self.last_seen = datetime.now()
            except Again:
                break
        self.printe([self.hote, data[str(self.hote.value)] if self.hote > 1 else data])
