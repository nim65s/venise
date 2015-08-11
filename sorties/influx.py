from numbers import Number

from influxdb import InfluxDBClient

from ..vmq import subscriber_parser
from .diff import Diff


def float_if_num(val):
    return float(val) if isinstance(val, Number) else val


class Influx(Diff):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = InfluxDBClient(database='venise')

    def diff(self, hote, key, data):
        self.client.write_points([{
                'measurement': key,
                'tags': {'host': hote.name},
                'fields': {'val%i' % i: float_if_num(d) for i, d in enumerate(data)} if isinstance(data, list) else {'val': float_if_num(data)},
                }])


if __name__ == '__main__':
    Influx(**vars(subscriber_parser.parse_args())).run()
