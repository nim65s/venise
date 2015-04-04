from argparse import ArgumentParser

from zmq import Context, SUB, SUBSCRIBE

from .settings import CURRENT_HOST, Hote, MAIN_HOST, PORT_SORTIES


class Subscriber(object):
    def __init__(self, hote, *args, **kwargs):
        self.context = Context()
        self.subscriber = self.context.socket(SUB)
        self.subscriber.connect("tcp://%s:%i" % (MAIN_HOST.name, PORT_SORTIES))
        self.subscriber.setsockopt_string(SUBSCRIBE, u'')  # TODO: les sorties devraient pouvoir override ça
        self.hote = Hote[hote]
        self.data = {}

    def sub(self):
        data = self.subscriber.recv_json()
        if self.hote > 0:
            data = data[self.hote]
        self.data.update(**data)

subscriber_parser = ArgumentParser(conflict_handler='resolve')
subscriber_parser.add_argument('-H', '--host', help="hôte source", default=CURRENT_HOST.name, choices=[h.name for h in Hote])
