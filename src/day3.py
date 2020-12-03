#!python3

""" 
Advent of code 2020

Day 3: Toboggan Trajector  
"""

from argparse import ArgumentParser
import logging
import math
import os
import sys


LOG = logging.getLogger(__name__)


class Map():

    def __init__(self, fn):
        with open(fn) as fh:
            self.lines = [s.strip() for s in fh]
            self.xm = len(self.lines[0])
            self.ym = len(self.lines)

    def getxy(self, x, y):
        if y >= self.ym:
            return None
        x0 = x % self.xm
        line = self.lines[y]
        pt = line[x0]
        return pt

    def trees_per_slope(self, dx, dy):
        treecnt = 0
        x, y = (0, 0)
        while (pt := self.getxy(x, y)) is not None:
            if pt == "#":
                treecnt += 1
            x += dx
            y += dy
        return treecnt   
        

def part1():
    mp = Map(r"..\day3_input.txt")
    rc = mp.trees_per_slope(3, 1)
    LOG.info(f"{rc} trees")


def part2():
    mp = Map(r"..\day3_input.txt")
    results = list()
    for dx, dy in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        results.append(mp.trees_per_slope(dx, dy))
    rc = math.prod(results)
    for r in results:
        LOG.info(f"{r} trees")
    LOG.info(f"{rc} product")
   

def cli(argv=None):
    # command line interface
    if argv is None:
        argv = sys.argv
    LOG.info("%s %s", os.path.basename(argv[0]), " ".join(argv[1:]))
    parser = ArgumentParser(description="Advent of code 2020")
    parser.add_argument("-1", "--part1", action='store_true')
    parser.add_argument("-2", "--part2", action='store_true')
    args = parser.parse_args(argv[1:])
    argd = vars(args)
    if False:
        # arguments
        for k, v in argd.items(): 
            print(k, v)
        # enviroment
        for k, v in os.environ.items(): 
            print(k, v)
    # feature
    if args.part1:
        part1()
    if args.part2:
        part2()
    return 0


if __name__ == "__main__":
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s.%03d'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(process)i] %(levelname).4s %(module)s.%(funcName)s: %(message)s')
    sys.exit(cli())
