from numpy import mean, median, var

from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireDefault(Trajectoire):
    def process_speed(self, granier, **kwargs):
        return {
                'v': mean(granier),
                'w': median(granier),
                't': var(granier),
                }

if __name__ == '__main__':
    TrajectoireDefault(**vars(trajectoire_parser.parse_args())).loop()
