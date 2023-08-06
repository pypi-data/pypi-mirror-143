# -*- coding: utf-8 -*-
import sys
import logging
from argparse import ArgumentParser
from traceback import format_exc

from exonutils.service import BaseService, BaseServiceTask
from exonutils.buffers import FileBuffer

logging.basicConfig(
    level=logging.INFO, stream=sys.stdout,
    format='%(asctime)s [%(name)s] %(levelname)s %(message)s')


class Task1(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing writer")
        self.buff = FileBuffer('SampleBuffer')
        self.buff.set('counter_old', 0)

    def execute(self):
        global counter
        counter = self.buff.get('counter')

        if counter is None:
            self.buff.set('counter', 0)
        else:
            self.buff.set('counter_old', counter)
            self.buff.set('counter', counter + 1)

        self.sleep(5)

    def terminate(self):
        self.buff.purge()


class Task2(BaseServiceTask):

    def initialize(self):
        self.log.info("initializing reader")
        self.buff = FileBuffer('SampleBuffer')

    def execute(self):
        global counter
        self.log.info("buffer data\n%s" % '\n'.join(
            [" - %s = %s" % (k, v) for k, v in self.buff.items()]))
        self.sleep(2)

    # def terminate(self):
    #     self.log.info("terminating")


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.name = 'main'
    try:
        pr = ArgumentParser(prog=None)
        pr.add_argument('-x', dest='debug', action='store_true',
                        help='enable debug mode')
        args = pr.parse_args()

        if args.debug:
            logger.setLevel(logging.DEBUG)

        s = BaseService('FileBuffer', logger=logger)
        s.tasks = [Task1, Task2]
        s.start()

    except Exception:
        logger.fatal(format_exc())
        sys.exit(1)
