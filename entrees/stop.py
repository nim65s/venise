from .entree import Entree


class EntreeStop(Entree):
    def __init__(self, v, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {'v': v, 'stop': False}

    def send(self, value):
        self.push.send_json([self.hote, value])

    def loop(self):
        while True:
            r = input('→ ')
            if 'c' in r:
                self.send({})
                # TODO
