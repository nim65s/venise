from .manuel import TrajectoireManuelle as Trajectoire
from .trajectoire import trajectoire_parser as parser

if __name__ == '__main__':
    Trajectoire(**vars(parser.parse_args())).run()
