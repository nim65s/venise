from datetime import datetime

from ..vmq import Subscriber, Pusher


class Sortie(Subscriber, Pusher):
    def loop(self):
        self.sub()
        self.process(**self.data[self.hote])

    def process(self, **kwargs):
        raise NotImplementedError()

    def send(self, status):
        print(status)
        self.push.send_json([self.hote, {'status': status}])
