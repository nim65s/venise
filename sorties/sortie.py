from ..vmq import CacheRequester


class Sortie(CacheRequester):
    def loop(self):
        self.sub()
        self.process(**self.data[self.hote])

    def process(self, **kwargs):
        raise NotImplementedError()
