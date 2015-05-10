from numpy import array

from ..vmq import vmq_parser, Subscriber, Pusher


class Anomaly(Subscriber, Pusher):
    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            self.push.send_json([h, {'anomaly': self.check_anomaly(**self.data[h])}])

    def check_anomaly(self, vc, vm, **kwargs):
        vc, vm = array(vc), array(vm)
        return bool(abs((vc - vm) / vc).sum() > 1)


if __name__ == '__main__':
    Anomaly(**vars(vmq_parser.parse_args())).run()
