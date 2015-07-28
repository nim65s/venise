from datetime import datetime, timedelta

from numpy import array

from ..settings import Hote
from ..vmq import Pusher, Subscriber, vmq_parser

AU = 'Désarme l’arrête d’urgence et Appuie sur le bouton vert !'


class Anomaly(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anomaly = {h: None for h in self.hotes}
        self.is_boosting = {h: None for h in self.hotes}

    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            self.push.send_json([h, {'anomaly': self.check_anomaly(**self.data[h])}])

    def check_anomaly(self, vc, vm, hote, anomaly, stop, is_up, status, **kwargs):
        vc, vm, hote = array(vc), array(vm), Hote(hote)
        if 0 in vc:
            return False
        new_anomaly = bool(abs((vc - vm) / vc).sum() > 1) and not stop and is_up and status != AU
        if not new_anomaly:
            if self.anomaly[hote]:
                print('Fin de l’anomalie sur %s' % hote.name)
                self.anomaly[hote] = None
            if self.is_boosting[hote]:
                print('Fin du boost sur %s' % hote.name)
                self.push.send_json([hote, {'boost': False}])
                self.is_boosting[hote] = False
            return False
        if anomaly:
            if self.anomaly[hote] is None:
                self.anomaly[hote] = datetime.now()
                print('Ancienne anomalie récupérée sur %s' % hote.name)
            if datetime.now() - self.anomaly[hote] > timedelta(seconds=12) and self.is_boosting[hote]:
                print('Le BOOST sur %s a duré plus de 2s…' % hote.name)
                self.push.send_json([hote, {'boost': False}])
                return False
            elif datetime.now() - self.anomaly[hote] > timedelta(seconds=10) and hote != Hote.moro:
                print('L’anomalie sur %s a duré plus de 10s… BOOST !' % hote.name)
                self.is_boosting[hote] = True
                self.push.send_json([hote, {'boost': True}])
        else:
            self.anomaly[hote] = datetime.now()
            print('Nouvelle anomalie sur %s' % hote.name)
        return True


if __name__ == '__main__':
    Anomaly(**vars(vmq_parser.parse_args())).run()
