from .points import TrajectoirePoints, trajectoire_points_parser


class TrajectoireDemo(TrajectoirePoints):
    def get_w(self, gm, hote, **kwargs):
        return (-1) ** hote

if __name__ == '__main__':
    TrajectoireDemo(**vars(trajectoire_points_parser.parse_args())).run()
