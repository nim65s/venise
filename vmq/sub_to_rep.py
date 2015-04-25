from zmq import REP

from ..settings import PORT_CACHE
from .subscriber import Subscriber
from .vmq import vmq_parser


class CacheReponder(Subscriber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reponder = self.context.socket(REP)
        self.reponder.bind('tcp://*:%i' % PORT_CACHE)

    def loop(self):
        self.reponder.recv_json()
        self.sub()
        self.reponder.send_json(self.data)


if __name__ == '__main__':
    CacheReponder(**vars(vmq_parser.parse_args())).run()
