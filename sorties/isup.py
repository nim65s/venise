from datetime import datetime, timedelta

from ..vmq import Pusher, Subscriber, vmq_parser


class IsUp(Subscriber, Pusher):
    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            self.push.send_json([h, {'is_up': self.check_up(**self.data[h])}])

    def check_up(self, hote, last_seen_agv, **kwargs):
        return (datetime.now() - datetime.strptime(last_seen_agv, '%Y-%m-%d %H:%M:%S.%f')) < timedelta(seconds=2)


if __name__ == '__main__':
    IsUp(**vars(vmq_parser.parse_args())).run()
