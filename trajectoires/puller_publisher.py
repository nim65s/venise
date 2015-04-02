from zmq import Context, NOBLOCK, PUB, PULL
from zmq.error import Again

from .settings import Hote, PORT_ENTREES, PORT_SORTIES


class PullerPublisher(object):
    def __init__(self, *args, **kwargs):
        self.context = Context()

        self.publisher = self.context.socket(PUB)
        self.publisher.bind("tcp://*:%i" % PORT_SORTIES)

        self.puller = self.context.socket(PULL)
        self.puller.bind("tcp://*:%i" % PORT_ENTREES)

    def pull(self):
        ret = {i: {} for i in Hote}
        while True:
            try:
                num, datas = self.puller.recv_json(NOBLOCK)
                ret[num].update(**datas)
            except Again:
                break

    def pub(self):
        self.publisher.send_json(self.data)
