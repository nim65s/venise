from datetime import datetime, timedelta
from math import pi, copysign
from time import sleep
from socket import socket, timeout

from ..settings import HOST_AGV, PORT_AGV, PERIODE, SMOOTH_FACTOR
from ..vmq import vmq_parser
from .sortie import Sortie

now = datetime.now
per = timedelta(seconds=PERIODE)


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
        start = now()
        self.smoothe()
        try:
            self.socket.sendall(self.send_agv())
            ret = self.socket.recv(1024).decode('ascii')
            if ret.startswith('+'):  # Les erreurs commencent par un +
                code = int(ret[1:].split(',')[0])
                if code == 3:  # Joystick connecté
                    self.send('Déconnecte le joystick !')
                elif code == 4:  # Post-démarrage ou arrêt d’urgence
                    self.send('Appuie sur le bouton vert !')
                elif code == 5:  # Velocity too high
                    pass
                elif code == 10:  # no response from AGV software
                    self.connect()
                else:
                    raise RuntimeError(ret)
            else:
                self.send('OK')
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.send('%s Failed connection !' % now())
            self.connect()
        duree = now() - start
        reste = per - duree
        if reste > timedelta(0):
            sleep(reste.microseconds / 1000000)
        else:
            print('La boucle a mis beaucoup trop de temps:', duree)

    def send_agv(self):
        if self.data[self.hote]['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({v1}, {t1s}, {v2}, {t2s}, {v3}, {t3s})'
        return bytes(template.format(**self.data[self.hote]).encode('ascii'))

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
