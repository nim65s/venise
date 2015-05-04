from argparse import ArgumentParser

from .sonde import Sonde, sonde_parser
from ..settings import N_SONDES


class Granier(Sonde):
    def process_granier(self, granier, gmi, gma, gm, **kwargs):
        for i in range(N_SONDES):
            gmi[i] = min(granier[i], gmi[i])
            gma[i] = max(granier[i], gma[i])
            gm[i] = round((granier[i] - gmi[i]) / (gma[i] - gmi[i] if gma[i] != gmi[i] else 1), 5)
        return {'gma': gma, 'gmi': gmi, 'gm': gm}

granier_parser = ArgumentParser(parents=[sonde_parser], conflict_handler='resolve')
granier_parser.set_defaults(nom='granier', period=30, n_values=3, maxi=5, mini=0)
