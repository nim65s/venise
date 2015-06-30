from argparse import ArgumentParser
from logging import INFO, Formatter, getLogger
from logging.handlers import TimedRotatingFileHandler
from os.path import expanduser
from time import sleep

from ..vmq import Subscriber, vmq_parser


class SortieLog(Subscriber):
    def __init__(self, period, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.logger = getLogger(logger)
        self.logger.setLevel(INFO)
        handler = TimedRotatingFileHandler(expanduser('~/logs/%s-%i.log' % (logger, self.hote - 1)), when='midnight')
        handler.setLevel(INFO)
        handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def loop(self):
        self.sub(block=0)
        self.log(self.logger, **self.data[self.hote])
        sleep(self.period)

    def log(self, logger, erreurs, **kwargs):
        raise NotImplementedError()

logger_parser = ArgumentParser(parents=[vmq_parser], conflict_handler='resolve')
logger_parser.add_argument('--period', type=float, default=1)
logger_parser.add_argument('--logger', default='venise')

if __name__ == '__main__':
    SortieLog(**vars(logger_parser.parse_args())).run()
