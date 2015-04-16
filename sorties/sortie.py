from ..vmq import Subscriber


class Sortie(Subscriber):
    def loop(self):
        self.sub()
        self.process(**self.data[self.hote])

    def process(self, **kwargs):
        raise NotImplementedError()
