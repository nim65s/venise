from socket import socket, timeout

from ..settings import HOST_AGV, PORT_AGV
from ..vmq import vmq_parser
from .sortie import Sortie


class SortieAGV(Sortie):
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
                print('connecting... %s:%i' % (HOST_AGV[self.hote], PORT_AGV))
                self.socket.connect((HOST_AGV[self.hote], PORT_AGV))
                print('connected')
                break
            except timeout:
                print('timeout…')
            except ConnectionRefusedError:
                print('Connection Refused…')
            except BrokenPipeError:
                print('Broken pipe…')

    def process(self, **kwargs):
        try:
            self.socket.sendall(self.send_agv())
            ret = self.socket.recv(1024).decode('ascii')
            if ret.startswith('+'):  # Les erreurs commencent par un +
                code = int(ret[1:].split(',')[0])
                if code == 3:  # Joystick connecté
                    print('Déconnecte le joystick !')
                elif code == 4:  # Post-démarrage ou arrêt d’urgence
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
        if self.data[self.hote]['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({v1}, {t1}, {v2}, {t2}, {v3}, {t3})'
        return bytes(template.format(**self.data[self.hote]).encode('ascii'))

if __name__ == '__main__':
    SortieAGV(**vars(vmq_parser.parse_args())).run()
