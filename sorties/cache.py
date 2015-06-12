from ..settings import MAIN_HOST, PORT_PUSH, PROD
from ..vmq import Pusher, Subscriber, puller_parser


class Cache(Subscriber, Pusher):
    def __init__(self, port_push, *args, **kwargs):
        super().__init__(*args, port_push=port_push, **kwargs)
        url = 'tcp://%s:%i' % (self.hote.name if PROD else MAIN_HOST.name, PORT_PUSH + (not PROD and port_push) * 10 * self.hote)
        self.printe(url)
        self.push.connect(url)

    def loop(self):
        self.sub(block=0)
        self.push.send_json([self.hote, self.data[self.hote]])


if __name__ == '__main__':
    puller_parser.set_defaults(port_push=True)
    Cache(**vars(puller_parser.parse_args())).run()
