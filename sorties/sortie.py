from datetime import datetime, timedelta
from time import sleep

from ..vmq import Puller, Pusher
from ..settings import PERIODE

per = timedelta(seconds=PERIODE)


class Sortie(Puller, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_send = []

    def loop(self):
        start = datetime.now()
        self.pull()
        if datetime.now() - self.last_seen > timedelta(seconds=2):
            self.send('déconnecté du serveur')
        if datetime.now() - self.last_seen > timedelta(seconds=3):
            self.data[self.hote]['stop'] = True
        self.process(**self.data[self.hote])
        for var in self.to_send:
            self.push.send_json([self.hote, {var: self.data[self.hote][var]}])
        duree = datetime.now() - start
        reste = per - duree
        if reste < timedelta(0):
            self.send('La boucle a mis beaucoup trop de temps: %s' % duree)
        else:
            sleep(reste.microseconds / 1000000)

    def process(self, **kwargs):
        raise NotImplementedError()

    def send(self, val, var='status'):
        self.push.send_json([self.hote, {var: val}])
