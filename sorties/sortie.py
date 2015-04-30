from ..vmq import Puller, Pusher


class Sortie(Puller, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self, **kwargs):
        raise NotImplementedError()

    def send(self, val, var='status'):
        self.push.send_json([self.hote, {var: val}])
