from datetime import datetime

from zmq import NOBLOCK, SUB, SUBSCRIBE
from zmq.error import Again

from ..settings import AGV_HOST, PORT_PUB
from .vmq import VMQ


class Subscriber(VMQ):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.subscriber = self.context.socket(SUB)
        url = "tcp://%s:%i" % (main, PORT_PUB)
        self.log(url)
        self.subscriber.connect(url)
        self.subscriber.setsockopt_string(SUBSCRIBE, '')
        self.last_seen = datetime(1970, 1, 1)
        self.sub(block=0)

    def sub(self, block=NOBLOCK):
        while True:
            try:
                data = self.subscriber.recv_json(block)
                for h in self.hosts:
                    if str(h.value) in data:
                        self.data[h].update(**data[str(h.value)])
                self.last_seen = datetime.now()
                self.log([self.host, data[str(self.host.value)]
                          if AGV_HOST else data])
            except Again:
                break
            if not block:
                break
