from numpy import array
from datetime import datetime, timedelta

from ..vmq import vmq_parser, Subscriber, Pusher
from ..settings import Hote


class Anomaly(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anomaly = {h: None for h in self.hotes}
        self.is_boosting = {h: None for h in self.hotes}

    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            self.push.send_json([h, {'anomaly': self.check_anomaly(**self.data[h])}])

    def check_anomaly(self, vc, vm, hote, anomaly, **kwargs):
        vc, vm = array(vc), array(vm)
        new_anomaly = bool(abs((vc - vm) / vc).sum() > 1)
        if not new_anomaly:
            if self.anomaly[hote]:
                print('Fin de l’anomalie sur %s' % hote)
                self.anomaly[hote] = None
            if self.is_boosting[hote]:
                print('Fin du boost sur %s' % hote)
                self.push.send_json([h, {'boost': False}])
                self.is_boosting[hote] = False
            return False
        if anomaly:
            if datetime.now() - self.anomaly[hote] > timedelta(seconds=13) and self.is_boosting[hote]:
                print('Le BOOST sur %s a duré plus de 3s…' % hote)
                self.push.send_json([h, {'boost': False}])
                return False
            elif datetime.now() - self.anomaly[hote] > timedelta(seconds=10) and hote != Hote.moro:
                print('L’anomalie sur %s a duré plus de 10s… BOOST !' % hote)
                self.is_boosting[hote] = True
                self.push.send_json([h, {'boost': True}])
        else:
            self.anomaly[hote] = datetime.now()
            print('Nouvelle anomalie sur %s' % hote)
        return True


if __name__ == '__main__':
    Anomaly(**vars(vmq_parser.parse_args())).run()
