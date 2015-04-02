from .subscriber import Subscriber


class Sortie(Subscriber):
    def loop(self):
        while True:
            self.sub()
            self.process(**self.data)

    def process(self):
        raise NotImplementedError()
