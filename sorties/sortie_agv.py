from datetime import datetime, timedelta
from math import pi
from socket import socket, timeout
from time import sleep

from numpy import array, where, logical_and

from ..settings import HOST_AGV, PERIODE, PORT_AGV, SMOOTH_FACTOR, VIT_LIM_REV
from ..vmq import vmq_parser
from ..utils.dist_angles import dist_angles
from .sortie import Sortie

now = datetime.now
per = timedelta(seconds=PERIODE / 2)


class SortieAGV(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()
        self.to_send = ['vc', 'tc', 'tm', 'nt', 'reversed']
        self.data[self.hote]['reversed'] = [False, False, False]

    def loop(self):
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
            self.push.send_json([self.hote, {var: self.data[self.hote][var].round(5).tolist()}])
        self.push.send_json([self.hote, {'last_seen_agv': str(now())}])

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

    def process(self, reverse, smoothe, hote, **kwargs):
        self.data[hote].update(**self.recv_agv())
        self.data[hote].update(**self.copy_consignes(**self.data[hote]))
        if reverse:
            self.data[hote].update(**self.reverse(**self.data[hote]))
        if smoothe:
            self.data[hote].update(**self.smoothe(**self.data[hote]))
        self.socket.sendall(self.send_agv(**self.data[hote]))
        self.check_ret(self.socket.recv(1024).decode('ascii'))

    def recv_agv(self):
        self.socket.sendall('getPosition()'.encode('ascii'))
        pos = self.socket.recv(1024).decode('ascii').replace('\x00', '').split(',')
        angles = [float(i.strip()) for i in pos[1:]]
        return {
                'tm': array([a % (2 * pi) for a in angles]),
                'nt': array([a // (2 * pi) for a in angles]).astype(int),
                }

    def copy_consignes(self, vt, tt, reversed, **kwargs):
        return {'vc': array(vt), 'tc': array(tt), 'reversed': array(reversed)}

    def reverse(self, vc, tc, tm, reversed, **kwargs):
        vc[where(reversed)] *= -1
        tc[where(reversed)] += pi
        tc[where(reversed)] %= 2 * pi
        rev = abs(dist_angles(tm, tc)) > 2 * pi / 3
        vc[where(rev)] *= -1
        tc[where(rev)] += pi
        tc[where(rev)] %= 2 * pi
        reversed ^= rev
        return {'vc': vc, 'reversed': reversed}

    def smoothe(self, tm, tc, **kwargs):
        dst = dist_angles(tm, tc)
        return {'tc': tc if abs(dst).max() < SMOOTH_FACTOR else (tm - SMOOTH_FACTOR * dst / abs(dst).max()) % (2 * pi)}

    def send_agv(self, stop, vc, tc, **kwargs):
        if stop or abs(vc).sum() < 10:
            return b'stop()'
        template = 'setSpeedAndPosition({vc[0]}, {tc[0]}, {vc[1]}, {tc[1]}, {vc[2]}, {tc[2]})'
        return bytes(template.format(vc=vc, tc=tc).encode('ascii'))

    def check_ret(self, ret):
        if not ret.startswith('+'):  # Les erreurs commencent par un +
            self.send(ret.split(',')[1])
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

if __name__ == '__main__':
    SortieAGV(**vars(vmq_parser.parse_args())).run()
