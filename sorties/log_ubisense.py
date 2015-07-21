from math import hypot

from .log import SortieLog, logger_parser


class LogUbisense(SortieLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos = 0, 0, 0

    def log(self, logger, x, y, a, **kwargs):
        if self.pos != (x, y, a):
            log = logger.warning if hypot(x - self.pos[0], y - self.pos[1]) > 0.1 else logger.info
            log('\t%.2f\t%.2f\t%.2f' % (x, y, a))
            self.pos = x, y, a


if __name__ == '__main__':
    logger_parser.set_defaults(logger='ubisense', period=0)
    LogUbisense(**vars(logger_parser.parse_args())).run()
