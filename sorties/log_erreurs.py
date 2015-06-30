from .log import SortieLog, logger_parser


class LogErreur(SortieLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.erreurs = ''

    def log(self, logger, erreurs, **kwargs):
        if self.erreurs != erreurs:
            state = 'vt: {vt}, vc: {vc}, vm: {vm}'.format(**kwargs)
            log = logger.warning if erreurs.startswith('+') else logger.info
            log('%s -- %s' % (erreurs, state))
            self.erreurs = erreurs


if __name__ == '__main__':
    logger_parser.set_defaults(logger='erreurs_agv', period=0)
    LogErreur(**vars(logger_parser.parse_args())).run()
