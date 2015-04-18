from zmq import SUB, SUBSCRIBE

from ..settings import MAIN_HOST, PORT_SORTIES
from .vmq import VMQ


class Subscriber(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subscriber = self.context.socket(SUB)
        url = "tcp://%s:%i" % (MAIN_HOST.name, PORT_SORTIES)
        if self.verbosite > 2:
            print(url)
        self.subscriber.connect(url)
        self.subscriber.setsockopt_string(SUBSCRIBE, '')  # TODO: les sorties devraient pouvoir override ça

    def sub(self):
        data = self.subscriber.recv_json()
        for h in self.hotes:
            if str(h.value) in data:
                self.data[h].update(**data[str(h.value)])
        self.print([self.hote, data[str(self.hote.value)] if self.hote > 1 else data])
