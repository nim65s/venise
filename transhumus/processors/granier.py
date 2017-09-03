from argparse import ArgumentParser

from ..settings import N_PROBES
from .processor import Processor, processor_parser


class Granier(Processor):
    def process(self, granier, gmi, gma, gm, **kwargs):
        for i in range(N_PROBES):
            gmi[i] = min(granier[i], gmi[i])
            gma[i] = max(granier[i], gma[i])
            diff = gma[i] - gmi[i]
            gm[i] = round((granier[i] - gmi[i]) / diff, 5) if diff > .1 else 1
        return {'gma': gma, 'gmi': gmi, 'gm': gm}


g_parser = ArgumentParser(parents=[processor_parser], conflict_handler='resolve')
g_parser.set_defaults(name='granier', period=25, n_values=3, maxi=5, mini=0)

if __name__ == '__main__':
    Granier(**vars(g_parser.parse_args())).run()
