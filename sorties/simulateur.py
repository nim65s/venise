from datetime import datetime, timedelta
from math import pi
from time import sleep

from numpy import array, where

from ..settings import PERIODE, SMOOTH_FACTOR
from ..utils.dist_angles import dist_angles
from ..vmq import puller_parser
from .sortie import Sortie

now = datetime.now
per = timedelta(seconds=PERIODE * 2)


class Simulateur(Sortie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        except (ConnectionResetError, BrokenPipeError):
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

    def process(self, reverse, smoothe, hote, boost, arriere, **kwargs):
        self.data[hote].update(**self.recv_agv(**self.data[hote]))
        self.data[hote].update(**self.copy_consignes(**self.data[hote]))
        if reverse:
            self.data[hote].update(**self.reverse(**self.data[hote]))
        if smoothe:
            self.data[hote].update(**self.smoothe(**self.data[hote]))
        if boost:
            self.data[hote].update(**self.boost(**self.data[hote]))
        if arriere:
            self.data[hote].update(**self.arriere(**self.data[hote]))
        self.push.send_json([hote, {'erreurs': 'ok'}])

    def recv_agv(self, vc, tc, nt, **kwargs):
        return {
                'vm': vc,
                'tm': tc,
                'nt': nt,
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

    def smoothe(self, tm, tc, hote, **kwargs):
        dst = dist_angles(tm, tc)
        return {'tc': tc if abs(dst).max() < SMOOTH_FACTOR[hote] else (tm - SMOOTH_FACTOR[hote] * dst / abs(dst).max()) % (2 * pi)}

    def boost(self, tg, **kwargs):
        return {'vc': array([80, 80, 80]), 'tc': array([tg, tg, tg])}

    def arriere(self, vc, **kwargs):
        return {'vc': -vc}


if __name__ == '__main__':
    puller_parser.set_defaults(port_push=True)
    Simulateur(**vars(puller_parser.parse_args())).run()
