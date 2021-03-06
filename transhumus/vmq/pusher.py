from zmq import PUSH

from ..settings import PORT_PUSH
from .vmq import VMQ


class Pusher(VMQ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://%s:%i" % (self.main, PORT_PUSH))

    def send(self):
        for h in self.hosts:
            self.push.send_json([h, self.data[h]])
            self.log([h, self.data[h]])
