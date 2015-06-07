from datetime import datetime, timedelta

from numpy import array

from ..settings import Hote, MAIN_HOST, PORT_PUSH, PROD
from ..vmq import Pusher, Subscriber, vmq_parser


class Cache(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push.connect('tcp://%s:%i' % (self.hote.name if PROD else MAIN_HOST.name, PORT_PUSH + 10 * self.hote))

    def loop(self):
        self.sub()
        self.push.send_json([self.hote, self.data[self.hote]])


if __name__ == '__main__':
    Cache(**vars(vmq_parser.parse_args())).run()
