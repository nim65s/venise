from .log import SortieLog, logger_parser


class LogGranier(SortieLog):
    def log(self, logger, granier, **kwargs):
        logger.info(granier)

if __name__ == '__main__':
    logger_parser.set_defaults(logger='granier', period=30)
    LogGranier(**vars(logger_parser.parse_args())).run()
