from datetime import datetime, timedelta
from math import pi
from socket import socket, timeout
from time import sleep

from numpy import array, where, logical_and

from ..settings import HOST_AGV, PERIODE, PORT_AGV, SMOOTH_FACTOR, VIT_LIM_REV
from ..vmq import vmq_parser
from .sortie import Sortie

now = datetime.now
per = timedelta(seconds=PERIODE)


class SortieAGV(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()
        self.to_send = ['vc', 'tc', 'tm', 'nt', 'reversed']
        self.data[self.hote]['reversed'] = [False, False, False]

    def loop(self):
        start = datetime.now()
        self.pull()
        if datetime.now() - self.last_seen > timedelta(seconds=2):
            self.send('déconnecté du serveur')
        if datetime.now() - self.last_seen > timedelta(seconds=3):
            self.data[self.hote]['stop'] = True
        try:
            self.process(**self.data[self.hote])
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.send('%s Failed connection !' % now())
            self.connect()
        for var in self.to_send:
            self.push.send_json([self.hote, {var: self.data[self.hote][var]}])
        duree = datetime.now() - start
        reste = per - duree
        if reste < timedelta(0):
            self.send('La boucle a mis beaucoup trop de temps: %s' % duree)
        else:
            sleep(reste.microseconds / 1000000)

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
        self.recv_agv()
        self.data[self.hote]['tc'] = self.smoothe(*self.reverse())
        self.force()
        self.socket.sendall(self.send_agv())
        self.check_ret(self.socket.recv(1024).decode('ascii'))

    def check_ret(self, ret):
        if not ret.startswith('+'):  # Les erreurs commencent par un +
            self.send('OK')
            return
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

    def send_agv(self):
        if self.data[self.hote]['stop']:
            return b'stop()'
        template = 'setSpeedAndPosition({vc[0]}, {tc[0]}, {vc[1]}, {tc[1]}, {vc[2]}, {tc[1]})'
        return bytes(template.format(**self.data[self.hote]).encode('ascii'))

    def recv_agv(self):
        self.socket.sendall('getPosition()'.encode('ascii'))
        pos = self.socket.recv(1024).decode('ascii').replace('\x00', '').split(',')
        angles = [float(i.strip()) for i in pos[1:]]
        self.data[self.hote]['tm'] = [round(a % (2 * pi), 4) for a in angles]
        self.data[self.hote]['nt'] = [int(a // (2 * pi)) for a in angles]

    def reverse(self):
        vc, tt, tm = array(self.data[self.hote]['vt']), array(self.data[self.hote]['tt']), array(self.data[self.hote]['tm'])
        dst = tm - tt
        rev = logical_and(dst > 2 * pi / 3, abs(vc) > VIT_LIM_REV)
        vc[where(rev)] *= -1
        tt[where(rev)] += pi
        tt[where(rev)] %= 2 * pi
        self.data[self.hote]['vc'] = vc.tolist()
        self.data[self.hote]['reversed'] = rev.tolist()
        return tm, tt

    def smoothe(self, tm, tt):
        dst = tm - tt
        if abs(dst).max() < SMOOTH_FACTOR:
            return tt.tolist()
        while (dst < -pi).any():
            dst[where(dst < -pi)] += 2 * pi
        while (dst > pi).any():
            dst[where(dst > pi)] -= 2 * pi
        return ((tm - SMOOTH_FACTOR * dst / abs(dst).max()) % (2 * pi)).round(5).tolist()

    def force(self):
        if not self.data[self.hote]['force']:
            return
        if abs(array(self.data[self.hote]['tt']) - array(self.data[self.hote]['tm'])) < 0.01:
            self.push.send_json([self.hote, {'force': False}])
            return
        self.data['vc'] = [5, 5, 5]
        self.data['tc'] = self.data['tt']


if __name__ == '__main__':
    SortieAGV(**vars(vmq_parser.parse_args())).run()
