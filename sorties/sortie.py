from datetime import datetime

from ..vmq import CacheRequester, Pusher


class Sortie(CacheRequester, Pusher):
    def loop(self):
        self.sub()
        self.process(**self.data[self.hote])

    def process(self, **kwargs):
        raise NotImplementedError()

    def send(self, event):
        self.push.send_json([self.hote, {'event': '%s %s' % (datetime.now().strftime('%H:%M'), event)}])
