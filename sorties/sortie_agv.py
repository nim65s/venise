import socket

from .settings import AGV_HOST, AGV_PORT, hosts
from .sortie import Sortie


class SortieAGV(Sortie):
    def __init__(self, *args, **kwargs):
        super(SortieAGV, self).__init__()
        self.socket = socket.socket()
        print('connecting...')
        self.socket.connect((AGV_HOST, AGV_PORT))
        print('connected')

    def process(self):
        self.socket.sendall(self.send_agv())
        ret = self.socket.recv(1024)
        if ret.startswith('+'):  # Les erreurs commencent par un +
            print ret
            raise RuntimeError(ret)

    def send_agv(self):
        return u'setSpeedAndPosition({t1}, {v1}, {t2}, {v2}, {t3}, {v3})'.format(**self.state)
