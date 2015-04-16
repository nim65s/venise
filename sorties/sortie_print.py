from pprint import pprint

from ..vmq.subscriber import subscriber_parser
from .sortie import Sortie


class SortiePrint(Sortie):
    def process(self, **kwargs):
        pprint(self.data)

if __name__ == '__main__':
    SortiePrint(**vars(subscriber_parser.parse_args())).run()
