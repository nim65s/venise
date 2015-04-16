from ..vmq.subscriber import subscriber_parser as parser
from .sortie_print import SortiePrint as Sortie

if __name__ == '__main__':
    Sortie(**vars(parser.parse_args())).run()
