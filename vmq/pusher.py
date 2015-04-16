from pprint import pprint

from zmq import PUSH

from ..settings import Hote, MAIN_HOST, PORT_ENTREES
from .vmq import VMQ


class Pusher(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_ENTREES))

    def send(self, data):
        if self.verbosite > 1:
            pprint(data)
        elif self.verbosite > 0:
            print(data)
        self.push.send_json([self.hote, data])
