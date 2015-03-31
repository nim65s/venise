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
        while True:
            try:
                self.socket.close()
                self.socket = socket()
                self.socket.settimeout(2)
                print('connecting... %s:%i' % (AGV_HOST[self.host], AGV_PORT))
                self.socket.connect((AGV_HOST[self.host], AGV_PORT))
                print('connected')
                break
            except timeout:
                print('timeout…')
            except ConnectionRefusedError:
                print('Connection Refused…')
            except BrokenPipeError:
                print('Broken pipe…')

    def process(self):
        pprint(self.state)
        try:
            self.socket.sendall(self.send_agv())
            ret = self.socket.recv(1024).decode('ascii')
            if ret.startswith('+'):  # Les erreurs commencent par un +
                code = int(ret[1:].split(',')[0])
                print(ret)
                if code == 4:  # TODO: c’est quoi déjà ?
                    print('Appuie sur le bouton vert !')
                elif code == 5:  # Velocity too high
                    pass
                elif code == 10:  # no response from AGV software
                    self.connect()
                else:
                    raise RuntimeError(ret)
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.connect()

    def send_agv(self):
        if self.state['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({v1}, {t1}, {v2}, {t2}, {v3}, {t3})'
        return bytes(template.format(**self.state).encode('ascii'))

if __name__ == '__main__':
    SortieAGVPrint().loop()
