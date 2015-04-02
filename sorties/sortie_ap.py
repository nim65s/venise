import sys
from pprint import pprint
from socket import socket, timeout

from .settings import HOST_AGV, hosts, PORT_AGV
from .sortie import Sortie


class SortieAGVPrint(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()

    def connect(self):
        while True:
            try:
                self.socket.close()
                self.socket = socket()
                self.socket.settimeout(2)
                print('connecting... %s:%i' % (HOST_AGV[self.host], PORT_AGV))
                self.socket.connect((HOST_AGV[self.host], PORT_AGV))
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
                if code == 4:  # Post-démarrage ou arrêt d’urgence
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
    if len(sys.argv) == 2:
        SortieAGVPrint(host=hosts[sys.argv[1]]).loop()
    else:
        SortieAGVPrint().loop()
