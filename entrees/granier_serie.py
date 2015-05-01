from argparse import ArgumentParser
from datetime import datetime
from os.path import expanduser

from serial import Serial

from .granier import Granier, granier_parser


class GranierSerie(Granier):
    def __init__(self, port, fichier, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = Serial('/dev/ttyUSB%i' % port, 38400)
        self.fichier = expanduser(fichier % self.hote)

    def process(self, value):
        l = self.serial.readline().decode('ascii').replace('\x00', '').replace('\x04', '').split()
        try:
            datetime.strptime(' '.join(l[:2]), '%d-%m-%y %H:%M:%S')
        except:
            print('fail:', l)
            return {}
        with open(self.fichier, 'a') as f:
            print(';'.join(l[:5]), file=f)
        return [round(float(l[2 + s]), 5) for s in range(3)]

    def fin(self):
        self.serial.close()

granier_serie_parser = ArgumentParser(parents=[granier_parser], conflict_handler='resolve')
granier_serie_parser.add_argument('-p', '--port', type=int, default=0)
granier_serie_parser.add_argument('-f', '--fichier', default='~/logs/granier_%i.log', help="fichier d’enregistrement des sondes")
granier_serie_parser.set_defaults(period=30, maxi=1)

if __name__ == '__main__':
    GranierSerie(**vars(granier_serie_parser.parse_args())).run()
