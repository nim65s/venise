from datetime import datetime, timedelta

from ..vmq import Pusher, Subscriber, vmq_parser


class IsUp(Subscriber, Pusher):
    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            is_up = self.check_up(**self.data[h])
            self.push.send_json([h, {'is_up': is_up}])
            if not is_up:
                self.push.send_json([h, {'status': 'AGV éteint'}])

    def check_up(self, hote, last_seen_agv, **kwargs):
        try:
            return (datetime.now() - datetime.strptime(last_seen_agv, '%Y-%m-%d %H:%M:%S.%f')) < timedelta(seconds=3)
        except:
            return False


if __name__ == '__main__':
    IsUp(**vars(vmq_parser.parse_args())).run()
