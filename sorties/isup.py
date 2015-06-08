from datetime import datetime, timedelta

from numpy import array

from ..settings import Hote
from ..vmq import Pusher, Subscriber, vmq_parser


class IsUp(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_seen_agvs = {h: datetime.min for h in self.hotes}

    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            self.push.send_json([h, {'is_up': self.check_up(**self.data[h])}])

    def check_up(self, hote, last_seen_agv, **kwargs):
        lsa = datetime.strptime(last_seen_agv, '%Y-%m-%d %H:%M:%S.%f')
        up = (lsa - self.last_seen_agvs[hote]) < timedelta(seconds=2)
        self.last_seen_agvs[hote] = lsa
        return up


if __name__ == '__main__':
    IsUp(**vars(vmq_parser.parse_args())).run()
