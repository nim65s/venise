from datetime import datetime, timedelta
from time import sleep

from ..vmq import Puller, Pusher
from ..settings import PERIODE

per = timedelta(seconds=PERIODE)

class Sortie(Puller, Pusher):
    def loop(self):
        start = datetime.now()
        self.pull()
        if datetime.now() - self.last_seen > timedelta(seconds=2):
            self.send('déconnecté du serveur')
            self.data[self.hote]['stop'] = True
        self.process(**self.data[self.hote])
        duree = datetime.now() - start
        reste = per - duree
        if reste < timedelta(0):
            self.send('La boucle a mis beaucoup trop de temps: %s' % duree)
        else:
            sleep(reste.microseconds / 1000000)

    def process(self, **kwargs):
        raise NotImplementedError()

    def send(self, status):
        print(status)
        self.push.send_json([self.hote, {'status': status}])
