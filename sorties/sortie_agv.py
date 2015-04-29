from datetime import datetime
from math import pi
from socket import socket, timeout

from numpy import array, where, copysign

from ..settings import HOST_AGV, PORT_AGV, SMOOTH_FACTOR
from ..vmq import vmq_parser
from .sortie import Sortie

now = datetime.now


class SortieAGV(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()
        self.to_send = ['tc', 'tm', 'nt']

    def connect(self):
        while True:
            try:
                self.socket.close()
                self.socket = socket()
                self.socket.settimeout(2)
                self.send('%s connecting... %s:%i' % (now(), self.hote.name, PORT_AGV))
                self.socket.connect((HOST_AGV, PORT_AGV))
                self.send('%s connected' % now())
                break
            except timeout:
                self.send('%s timeout…' % now())
            except ConnectionRefusedError:
                self.send('%s Connection Refused…' % now())
            except BrokenPipeError:
                self.send('%s Broken pipe…' % now())

    def process(self, **kwargs):
        self.data[self.hote]['tc'] = self.smoothe()
        try:
            self.recv_agv()
            self.socket.sendall(self.send_agv())
            ret = self.socket.recv(1024).decode('ascii')
            if ret.startswith('+'):  # Les erreurs commencent par un +
                code = int(ret[1:].split(',')[0])
                if code == 2:  # Wrong number or format of arguments
                    self.send('Mauvais format d’envoi à BA !')
                    raise AttributeError
                elif code == 3:  # Joystick connecté
                    self.send('Déconnecte le joystick !')
                elif code == 4:  # Post-démarrage ou arrêt d’urgence
                    self.send('Désarme l’arrête d’urgence et Appuie sur le bouton vert !')
                elif code == 5:  # Velocity ou angle too high
                    pass
                elif code == 6:  # Initialisation ongoing
                    self.send('Initialisation en cours…')
                elif code == 7:  # Trop de tours
                    self.send('Trop de tours !')
                else:
                    raise RuntimeError(ret)
            else:
                self.send('OK')
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.send('%s Failed connection !' % now())
            self.connect()

    def send_agv(self):
        if self.data[self.hote]['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({vt[0]}, {tc[0]}, {vt[1]}, {tc[1]}, {vt[2]}, {tc[1]})'
        return bytes(template.format(**self.data[self.hote]).encode('ascii'))

    def recv_agv(self):
        self.socket.sendall('getPosition()'.encode('ascii'))
        pos = self.socket.recv(1024).decode('ascii').replace('\x00', '').split(',')
        angles = [float(i.strip()) for i in pos[1:]]
        self.data[self.hote]['tm'] = [round(a % (2 * pi), 4) for a in angles]
        self.data[self.hote]['nt'] = [int(a // (2 * pi)) for a in angles]

    def smoothe(self):
        tm, tt = array(self.data[self.hote]['tm']), array(self.data[self.hote]['tt'])
        dst = tm - tt
        if abs(dst).max() < SMOOTH_FACTOR:
            return tt.tolist()
        while (dst < -pi).any():
            dst[where(dst < -pi)] += 2 * pi
        while (dst > pi).any():
            dst[where(dst > pi)] -= 2 * pi
        return ((tm % (2 * pi) - SMOOTH_FACTOR * dst / dst.max()) % (2 * pi)).round(5).tolist()

if __name__ == '__main__':
    SortieAGV(**vars(vmq_parser.parse_args())).run()
