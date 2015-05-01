from pprint import pprint
from time import sleep

from ..settings import PERIODE
from ..vmq import Subscriber, vmq_parser


class SortiePrint(Subscriber):
    def loop(self):
        self.sub()
        pprint(self.data)
        sleep(PERIODE)


if __name__ == '__main__':
    SortiePrint(**vars(vmq_parser.parse_args())).run()
