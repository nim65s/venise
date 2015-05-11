from datetime import datetime, timedelta
from math import pi
from socket import socket, timeout
from time import sleep
from os.path import expanduser

from numpy import array, where, logical_and

from ..settings import HOST_AGV, PERIODE, PORT_AGV, SMOOTH_FACTOR, VIT_LIM_REV
from ..vmq import vmq_parser
from ..utils.dist_angles import dist_angles
from .sortie import Sortie

now = datetime.now
per = timedelta(seconds=PERIODE * 2)


class SortieAGV(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()
        self.to_send = ['vc', 'tc', 'vm', 'tm', 'nt', 'reversed']
        self.data[self.hote]['reversed'] = [False, False, False]

    def loop(self):
        start = now()
        self.pull()
        if datetime.now() - self.last_seen > timedelta(seconds=3):
            self.send('déconnecté du serveur')
        if datetime.now() - self.last_seen > timedelta(seconds=5):
            self.data[self.hote]['stop'] = True
        try:
            self.process(**self.data[self.hote])
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.send('%s Failed connection !' % now())
            self.connect()
        for var in self.to_send:
            self.push.send_json([self.hote, {var: array(self.data[self.hote][var]).round(5).tolist()}])
        self.push.send_json([self.hote, {'last_seen_agv': str(now())}])
        duree = now() - start
        reste = per - duree
        if reste < timedelta(0):
            self.send('Délai anormal…')
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
            except OSError:
                self.send('%s L’AGV ne répond pas…' % now())

    def process(self, reverse, smoothe, hote, boost, arriere, **kwargs):
        self.data[hote].update(**self.recv_agv())
        self.data[hote].update(**self.copy_consignes(**self.data[hote]))
        if reverse:
            self.data[hote].update(**self.reverse(**self.data[hote]))
        if smoothe:
            self.data[hote].update(**self.smoothe(**self.data[hote]))
        if boost:
            self.data[hote].update(**self.boost(**self.data[hote]))
        if arriere:
            self.data[hote].update(**self.arriere(**self.data[hote]))
        self.socket.sendall(self.send_agv(**self.data[hote]))
        self.check_ret(self.recv_rep())
        self.socket.sendall('getErrors()'.encode('ascii'))
        erreurs = self.recv_rep()
        self.push.send_json([hote, {'erreurs': 'ok' if erreurs.startswith('-') else erreurs}])

    def recv_rep(self):
        return self.socket.recv(1024).decode('ascii').replace('\x00', '')

    def recv_agv(self):
        self.socket.sendall('getSpeedAndPosition()'.encode('ascii'))
        pos = self.socket.recv(1024).decode('ascii').replace('\x00', '').split(',')
        v1, t1, v2, t2, v3, t3 = [float(i.strip()) for i in pos[1:]]
        return {
                'vm': array([v1, v2, v3]),
                'tm': array([a % (2 * pi) for a in [t1, t2, t3]]),
                'nt': array([a // (2 * pi) for a in [t1, t2, t3]]).astype(int),
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

    def boost(self, tg, **kwargs):
        return {'vc': array([80, 80, 80]), 'tc': array([tg, tg, tg])}

    def arriere(self, vc, **kwargs):
        return {'vc': -vc}

    def send_agv(self, stop, boost, vc, tc, **kwargs):
        if stop or abs(vc).sum() < 10:
            return b'stop()'
        cmd = 'setSpeedAndPositionCalibration' if boost else 'setSpeedAndPosition'
        template = '({vc[0]}, {tc[0]}, {vc[1]}, {tc[1]}, {vc[2]}, {tc[2]})'
        return bytes((cmd + template).format(vc=vc, tc=tc).encode('ascii'))

    def check_ret(self, ret):
        if not ret.startswith('+'):  # Les erreurs commencent par un +
            self.send(ret.split(',')[1].strip())
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
