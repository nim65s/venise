from ..settings import MAIN_HOST, PORT_PUSH, PROD
from ..vmq import puller_parser, Pusher, Subscriber


class Cache(Subscriber, Pusher):
    def __init__(self, port_push, *args, **kwargs):
        super().__init__(*args, port_push=port_push, **kwargs)
        url = 'tcp://%s:%i' % (self.hote.name if PROD else MAIN_HOST.name, PORT_PUSH + port_push * 10 * self.hote)
        self.printe(url)
        self.push.connect(url)

    def loop(self):
        self.sub(block=0)
        self.push.send_json([self.hote, self.data[self.hote]])


if __name__ == '__main__':
    Cache(**vars(puller_parser.parse_args())).run()
