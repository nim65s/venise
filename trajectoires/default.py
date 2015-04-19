from numpy import mean, median, var

from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireDefault(Trajectoire):
    def process_speed(self, granier, **kwargs):
        return {
                'v': round(mean(granier), 4),
                'w': round(median(granier), 4),
                't': round(var(granier), 4),
                }

if __name__ == '__main__':
    TrajectoireDefault(**vars(trajectoire_parser.parse_args())).run()
