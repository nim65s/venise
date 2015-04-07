from ..vmq.subscriber import Subscriber


class Sortie(Subscriber):
    def loop(self):
        while True:
            try:
                self.sub()
                self.process(**self.data)
            except KeyboardInterrupt:
                print()
                break

    def process(self, **kwargs):
        raise NotImplementedError()
