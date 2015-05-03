from . import Subscriber, Pusher, vmq_parser
from ..settings import PORT_PUSH


class Cacher(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push.connect("tcp://%s:%i" % (self.hote.name, PORT_PUSH))
        self.printe('Connection…')
        self.sub(block=0)
        self.printe('Connecté')

    def loop(self):
        self.sub()
        self.send()

if __name__ == '__main__':
    Cacher(**vars(vmq_parser.parse_args())).run()
