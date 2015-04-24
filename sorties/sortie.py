from time import sleep

from ..vmq import CacheRequester


class Sortie(CacheRequester):
    def loop(self):
        self.sub()
        self.process(**self.data[self.hote])
        sleep(0.1)

    def process(self, **kwargs):
        raise NotImplementedError()
