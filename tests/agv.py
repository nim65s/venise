from ..vmq import Puller, Pusher, vmq_parser
from datetime import datetime, timedelta
from pprint import pprint

class TestSortieAGV(Puller, Pusher):
    def loop(self):
        self.pull()
        self.process(**self.data[self.hote])


    def send(self, status):
        print(status)
        self.push.send_json([self.hote, {'status': status}])

    def process(self, **kwargs):
        pprint(self.data)
        self.send(datetime.now().strftime('%f'))


if __name__ == '__main__':
    TestSortieAGV(**vars(vmq_parser.parse_args())).run()
