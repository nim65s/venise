from pprint import pprint
from time import sleep

from ..settings import PERIOD
from ..vmq import Subscriber, parser


class PrintOutput(Subscriber):
    def loop(self):
        self.sub()
        pprint(self.data)
        sleep(PERIOD)


if __name__ == '__main__':
    PrintOutput(**vars(parser.parse_args())).run()
