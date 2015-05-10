from numpy import array
from datetime import datetime, timedelta

from ..vmq import vmq_parser, Subscriber, Pusher


class Anomaly(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anomaly = {h: None for h in self.hotes}

    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            self.push.send_json([h, {'anomaly': self.check_anomaly(**self.data[h])}])

    def check_anomaly(self, vc, vm, hote, anomaly, **kwargs):
        vc, vm = array(vc), array(vm)
        new_anomaly = bool(abs((vc - vm) / vc).sum() > 1)
        if not new_anomaly:
            return False
        if anomaly:
            if datetime.now() - self.anomaly[hote] > timedelta(seconds=13):
                self.push.send_json([h, {'boost': False}])
                return False
            elif datetime.now() - self.anomaly[hote] > timedelta(seconds=10):
                self.push.send_json([h, {'boost': True}])
        else:
            self.anomaly[hote] = datetime.now()
        return True


if __name__ == '__main__':
    Anomaly(**vars(vmq_parser.parse_args())).run()
