from pprint import pprint

from zmq import SUB, SUBSCRIBE

from ..settings import MAIN_HOST, PORT_SORTIES
from .vmq import VMQ


class Subscriber(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subscriber = self.context.socket(SUB)
        url = "tcp://%s:%i" % (MAIN_HOST.name, PORT_SORTIES)
        #print(url)
        self.subscriber.connect(url)
        self.subscriber.setsockopt_string(SUBSCRIBE, u'')  # TODO: les sorties devraient pouvoir override ça

    def sub(self):
        data = self.subscriber.recv_json()
        if self.hote > 0:
            data = data[str(self.hote.value)]
        self.data.update(**data)
