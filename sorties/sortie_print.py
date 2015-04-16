from pprint import pprint

from ..vmq import vmq_parser
from .sortie import Sortie


class SortiePrint(Sortie):
    def process(self, **kwargs):
        pprint(self.data)

if __name__ == '__main__':
    SortiePrint(**vars(vmq_parser.parse_args())).run()
