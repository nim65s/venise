from zmq import Context, SUB, SUBSCRIBE

from .settings import current_host, SORTIES_HOST, SORTIES_PORT


class Sortie(object):
    def __init__(self, host=None):
        self.host = current_host if host is None else host
        self.context = Context()
        self.subscriber = self.context.socket(SUB)
        self.subscriber.connect("tcp://%s:%i" % (SORTIES_HOST, SORTIES_PORT))
        self.subscriber.setsockopt_string(SUBSCRIBE, u'')

        self.state = {}

    def sub(self):
        data = self.subscriber.recv_json()
        if self.host > 0:
            data = data['%i' % self.host]
        self.state.update(**data)

    def loop(self):
        while True:
            self.sub()
            self.process()

    def process(self):
        raise NotImplementedError()
