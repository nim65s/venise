from pprint import pprint
from socket import socket, timeout
from time import sleep

from .settings import AGV_HOST, AGV_PORT
from .sortie import Sortie


class SortieAGVPrint(Sortie):
    def __init__(self, *args, **kwargs):
        super(SortieAGVPrint, self).__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()

    def connect(self):
        try_again = True
        while try_again:
            try:
                try_again = False
                self.socket.close()
                self.socket = socket()
                self.socket.settimeout(2)
                print('connecting... %s:%i' % (AGV_HOST[self.host], AGV_PORT))
                self.socket.connect((AGV_HOST[self.host], AGV_PORT))
                print('connected')
            except timeout:
                try_again = True
            except ConnectionRefusedError:
                sleep(5)

    def process(self):
        pprint(self.state)
        ret = ''
        try:
            self.socket.sendall(self.send_agv())
            ret = self.socket.recv(1024).decode('ascii')
        except ConnectionResetError:
            self.connect()
        except timeout:
            print('\t\t\ttimeout…')
            self.connect()
        if ret.startswith('+'):  # Les erreurs commencent par un +
            print(ret)
            if ret[1] != '4':
                raise RuntimeError(ret)

    def send_agv(self):
        if self.state['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({v1}, {t1}, {v2}, {t2}, {v3}, {t3})'
        return bytes(template.format(**self.state).encode('ascii'))
