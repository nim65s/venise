from datetime import datetime, timedelta
from math import pi
from socket import socket, timeout
from time import sleep

from numpy import array, where

from ..settings import HOST_AGV, PERIODE, PORT_AGV, SMOOTH_FACTOR
from ..utils.dist_angles import dist_angles
from ..vmq import parser
from .sortie import Sortie

now = datetime.now
per = timedelta(seconds=PERIODE * 2)

tau = 2 * pi


class SortieAGV(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket()
        self.connect()
        self.to_send = ['vc', 'tc', 'vm', 'tm', 'nt', 'reversed']
        self.data[self.host]['reversed'] = [False, False, False]

    def loop(self):
        start = now()
        self.pull()
        if datetime.now() - self.last_seen > timedelta(seconds=3):
            self.send('déconnecté du serveur')
        if datetime.now() - self.last_seen > timedelta(seconds=5):
            self.data[self.host]['stop'] = True
        try:
            self.process(**self.data[self.host])
        except (ConnectionResetError, timeout, BrokenPipeError):
            self.send('%s Failed connection !' % now())
            self.connect()
        for var in self.to_send:
            self.push.send_json([self.host, {var: array(self.data[self.host][var]).round(5).tolist()}])
        self.push.send_json([self.host, {'last_seen_agv': str(now())}])
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
                self.send('%s connecting... %s:%i' % (now(), self.host.name, PORT_AGV))
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
                self.send("%s AGV doesn't respond…" % now())

    def process(self, reverse, smoothe, host, boost, arriere, **kwargs):
        self.data[host].update(**self.recv_agv())
        self.data[host].update(**self.copy_consignes(**self.data[host]))
        if reverse:
            self.data[host].update(**self.reverse(**self.data[host]))
        if smoothe:
            self.data[host].update(**self.smoothe(**self.data[host]))
        if boost:
            self.data[host].update(**self.boost(**self.data[host]))
        if arriere:
            self.data[host].update(**self.arriere(**self.data[host]))
        self.socket.sendall(self.send_agv(**self.data[host]))
        self.check_ret(self.recv_rep())
        self.socket.sendall('getErrors()'.encode('ascii'))
        errors = self.recv_rep()
        self.push.send_json([host, {'errors': 'ok' if errors.startswith('-') else errors}])

    def recv_rep(self):
        return self.socket.recv(1024).decode('ascii').replace('\x00', '')

    def recv_agv(self):
        self.socket.sendall('getSpeedAndPosition()'.encode('ascii'))
        pos = self.socket.recv(1024).decode('ascii').replace('\x00', '').split(',')
        v1, t1, v2, t2, v3, t3 = [float(i.strip()) for i in pos[1:]]
        return {
                'vm': array([v1, v2, v3]),
                'tm': array([a % tau for a in [t1, t2, t3]]),
                'nt': array([a // tau for a in [t1, t2, t3]]).astype(int),
                }

    def copy_consignes(self, vt, tt, reversed, **kwargs):
        return {'vc': array(vt), 'tc': array(tt), 'reversed': array(reversed)}

    def reverse(self, vc, tc, tm, reversed, **kwargs):
        vc[where(reversed)] *= -1
        tc[where(reversed)] += pi
        tc[where(reversed)] %= tau
        rev = abs(dist_angles(tm, tc)) > tau / 3
        vc[where(rev)] *= -1
        tc[where(rev)] += pi
        tc[where(rev)] %= tau
        reversed ^= rev
        return {'vc': vc, 'reversed': reversed}

    def smoothe(self, tm, tc, host, **kwargs):
        dst = dist_angles(tm, tc)
        tc = tc if abs(dst).max() < SMOOTH_FACTOR[host] else (tm - SMOOTH_FACTOR[host] * dst / abs(dst).max()) % tau
        return {'tc': tc}

    def boost(self, tg, **kwargs):
        return {'vc': array([80, 80, 80]), 'tc': array([tg, tg, tg])}

    def arriere(self, vc, **kwargs):
        return {'vc': -vc}

    def send_agv(self, stop, boost, vc, tc, **kwargs):
        if stop or abs(vc).sum() < 15:
            return b'stop()'
        cmd = 'setSpeedAndPositionCalibration' if boost else 'setSpeedAndPosition'
        template = '({vc[0]}, {tc[0]}, {vc[1]}, {tc[1]}, {vc[2]}, {tc[2]})'
        return bytes((cmd + template).format(vc=vc, tc=tc).encode('ascii'))

    def check_ret(self, ret):
        if not ret.startswith('+'):  # Errors starts with a +
            self.send(ret.split(',')[1].strip())
            return
        code = int(ret[1:].split(',')[0])
        if code == 2:  # Wrong number or format of arguments
            self.send('Wrong format for sending orders to the AGV !')
            raise AttributeError
        elif code == 3:
            self.send('Disconnect the joystick!')
        elif code == 4:
            self.send('Disarm the kill switch and Push the green button !')
        elif code == 5:  # Velocity or angle too high
            pass
        elif code == 6:
            self.send('Initialisation ongoing…')
        elif code == 7:
            self.send('Too much tours for the turrets !')
        else:
            raise RuntimeError(ret)


if __name__ == '__main__':
    SortieAGV(**vars(parser.parse_args())).run()
