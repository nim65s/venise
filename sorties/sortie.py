from datetime import datetime

from ..vmq import Puller, Pusher


class Sortie(Puller, Pusher):
    def loop(self):
        self.pull()
        self.process(**self.data[self.hote])

    def process(self, **kwargs):
        raise NotImplementedError()

    def send(self, status):
        print(status)
        self.push.send_json([self.hote, {'status': status}])
