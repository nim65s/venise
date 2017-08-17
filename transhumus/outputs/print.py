from pprint import pprint
from time import sleep

from ..settings import PERIOD
from ..vmq import Subscriber, vmq_parser


class PrintOutput(Subscriber):
    def loop(self):
        self.sub()
        pprint(self.data)
        sleep(PERIOD)


if __name__ == '__main__':
    PrintOutput(**vars(vmq_parser.parse_args())).run()
