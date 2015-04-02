from .agv import entree_agv_parser as parser
from .agv import EntreeAGV as Entree

if __name__ == '__main__':
    Entree(**vars(parser.parse_args())).loop()
