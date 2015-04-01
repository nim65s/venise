from argparse import ArgumentParser

from zmq import Context, PUSH

from .settings import CURRENT_HOST, Hote, MAIN_HOST, PORT_ENTREES


class Pusher(object):
    def __init__(self, host, *args, **kwargs):
        self.host = Hote[host]
        self.context = Context()
        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://%s:%i" % (MAIN_HOST.value, PORT_ENTREES))

    def send(self, data):
        self.push.send_json([self.host, data])


pusher_parser = ArgumentParser(add_help=False)
pusher_parser.add_argument('-H', '--host', help="hôte source", default=CURRENT_HOST.name)
