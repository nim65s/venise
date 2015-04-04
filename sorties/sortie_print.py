from pprint import pprint

from .sortie import Sortie
from .subscriber import subscriber_parser


class SortiePrint(Sortie):
    def process(self):
        pprint(self.state)

if __name__ == '__main__':
    SortiePrint(**vars(subscriber_parser.parse_args())).loop()
