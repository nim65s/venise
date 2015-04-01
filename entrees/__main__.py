from .agv import entree_agv_parser as parser
from .agv import EntreeAGV as entree

if __name__ == '__main__':
    entree(**vars(parser.parse_args())).loop()
