from time import sleep

from zmq import Context, PUSH

from .settings import current_host, ENTREES_HOST, ENTREES_PORT


class Entree(object):
    def __init__(self, nom, host=None, period=0, mini=-1, maxi=1, n_values=1):
        self.nom, self.host, self.period = nom, current_host if host is None else host, period
        self.mini, self.maxi, self.n_values, self.value = mini, maxi, n_values, [0] * n_values
        self.context = Context()
        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://%s:%i" % (ENTREES_HOST, ENTREES_PORT))

    def send(self, value):
        self.push.send_json([self.host, {self.nom: value}])

    def loop(self):
        while self.period:
            self.send(self.check_value(self.process()))
            sleep(self.period)

    def check_value(self, value):
        if len(value) != self.n_values:
            raise ValueError('%s sur %s: len(%r) != %i' % (self.nom, self.host.name, value, self.n_values))
        for i, v in enumerate(value):
            if not self.mini <= v <= self.maxi:
                raise ValueError('%s.%i sur %s: %f pas entre %f et %f' % (self.nom, i, self.host.name, v, self.mini, self.maxi))
        self.value = value
        return value

    def process(self):
        raise NotImplementedError()
