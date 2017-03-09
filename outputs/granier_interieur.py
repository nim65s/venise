from numpy import array
from time import sleep

from ..vmq import vmq_parser, Subscriber, Pusher
from ..settings import Hote, N_SONDES


class SortieGranierInterieur(Subscriber, Pusher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hote = Hote.moro
        self.hotes = [Hote.ame, Hote.yuki]

    def loop(self):
        self.sub()
        self.data[self.hote].update(**self.process_granier_interieur(**self.data[self.hote]))
        sleep(15)

    def process_granier_interieur(self, granier, gmi, gma, gm, **kwargs):
        granier = array([self.data[h]['granier'] for h in self.hotes]).mean(axis=0).round(3).tolist()
        for i in range(N_SONDES):
            gmi[i] = min(granier[i], gmi[i])
            gma[i] = max(granier[i], gma[i])
            gm[i] = round((granier[i] - gmi[i]) / (gma[i] - gmi[i] if gma[i] != gmi[i] else 1), 5)
        d = {'granier': granier, 'gma': gma, 'gmi': gmi, 'gm': gm}
        self.push.send_json([self.hote, d])
        return d


if __name__ == '__main__':
    SortieGranierInterieur(**vars(vmq_parser.parse_args())).run()
