from datetime import datetime
from os.path import expanduser

from ..vmq import Subscriber, vmq_parser


class LogErreur(Subscriber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.erreurs = {h: '' for h in self.hotes}

    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            if self.erreurs[h] != self.data[h]['erreurs']:
                self.erreurs[h] = self.data[h]['erreurs']
                with open(expanduser('~/log_erreurs_agv_%i' % (h - 1)), 'a') as f:
                    print('%s: %s' % (datetime.now().strftime('%Y/%m/%d %H:%M:%S'), self.erreurs[h]), file=f)


if __name__ == '__main__':
    LogErreur(**vars(vmq_parser.parse_args())).run()
