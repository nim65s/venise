from argparse import ArgumentParser

from .processor import Processor, processor_parser
from ..inputs.probe import probe_parser
from ..settings import N_PROBES


class Granier(Processor):
    def process(self, granier, gmi, gma, gm, **kwargs):
        for i in range(N_PROBES):
            gmi[i] = min(granier[i], gmi[i])
            gma[i] = max(granier[i], gma[i])
            gm[i] = round((granier[i] - gmi[i]) / (gma[i] - gmi[i]), 5) if gma[i] - gmi[i] > .1 else 1
        return {'gma': gma, 'gmi': gmi, 'gm': gm}


granier_parser = ArgumentParser(parents=[processor_parser], conflict_handler='resolve')
granier_parser.set_defaults(name='granier', period=25, n_values=3, maxi=5, mini=0)

if __name__ == '__main__':
    Granier(**vars(granier_parser.parse_args())).run()
