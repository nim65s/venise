from datetime import datetime, timedelta
from math import pi, copysign
from time import sleep
from socket import socket, timeout

from ..settings import HOST_AGV, PORT_AGV, PERIODE, SMOOTH_FACTOR
from ..vmq import vmq_parser
from .sortie import Sortie

now = datetime.now


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
        self.smoothe()
        try:
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
                elif code == 6:  #Initialisation ongoing
                    self.send('Initialisation en cours…')
                elif code == 7:  # Trop de tours
                    self.send('Trop de tours !')
                else:
                    raise RuntimeError(ret)
            else:
                self.send('OK')
            self.recv_agv()
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.send('%s Failed connection !' % now())
            self.connect()

    def send_agv(self):
        if self.data[self.hote]['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({v1}, {t1s}, {v2}, {t2s}, {v3}, {t3s})'
        return bytes(template.format(**self.data[self.hote]).encode('ascii'))

    def recv_agv(self):
        self.socket.sendall('getPosition()'.encode('ascii'))
        pos = self.socket.recv(1024).decode('ascii').replace('\x00', '').split(',')
        self.send([float(i.strip()) for i in pos[1:]], 'tr')


    def smoothe(self):
        for i in range(1, 4):
            vt, vts = 't%i' % i, 't%is' % i
            t = self.data[self.hote][vt]
            if vts not in self.data[self.hote]:
                self.data[self.hote][vts] = t
                continue
            ts = self.data[self.hote][vts]
            dst = ts - t
            if abs(dst) < SMOOTH_FACTOR:
                self.data[self.hote][vts] = t
                continue
            while dst < -pi:
                dst += 2 * pi
            while dst > pi:
                dst -= 2 * pi
            ts = round((ts - copysign(SMOOTH_FACTOR, dst)) % (2 * pi), 5)
            self.data[self.hote][vts] = ts
        self.push.send_json([self.hote, {key: self.data[self.hote][key] for key in ['t1s', 't2s', 't3s']}])

if __name__ == '__main__':
    SortieAGV(**vars(vmq_parser.parse_args())).run()
