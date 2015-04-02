from .trajectoire import Trajectoire, trajectoire_parser


class TrajectoireManuelle(Trajectoire):
    def process_speed(self, **kwargs):
        return {}

if __name__ == '__main__':
    TrajectoireManuelle(**vars(trajectoire_parser.parse_args())).loop()
