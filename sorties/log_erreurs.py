from log import SortieLog, logger_parser


class LogErreur(SortieLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.erreurs = {h: '' for h in self.hotes}

    def loop(self):
        self.sub(block=0)
        for h in self.hotes:
            if self.erreurs[h] != self.data[h]['erreurs']:
                self.erreurs[h] = self.data[h]['erreurs']
                with open(expanduser('~/logs/%i.log' % (h - 1)), 'a') as f:
                    state = 'vt: {vt}, vc: {vc}, vm: {vm}'.format(**self.data[h])
                    print('%s: %s -- %s' % (datetime.now().strftime('%Y/%m/%d %H:%M:%S'), self.erreurs[h], state), file=f)


if __name__ == '__main__':
    logger_parser.set_defaults(logger='erreurs_agv', period=0)
    LogErreur(**vars(logger_parser.parse_args())).run()
