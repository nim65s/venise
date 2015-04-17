from zmq import PUSH

from ..settings import MAIN_HOST, PORT_ENTREES
from .vmq import VMQ


class Pusher(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_ENTREES))

    def send(self):
        for h in self.hotes:
            self.push.send_json([h, self.data[h]])
            self.print([h, self.data[h]])
