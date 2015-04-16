from zmq import PUSH

from ..settings import MAIN_HOST, PORT_ENTREES
from .vmq import VMQ


class Pusher(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_ENTREES))

    def send(self, data):
        self.push.send_json([self.hote, data])
        self.print([self.hote, data])
