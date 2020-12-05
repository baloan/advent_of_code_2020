#!python3
# Created 5 Dec 2020
# @author: andreas

#!python3
# Created 5 Dec 2020
# @author: andreas

""" Advent of code 2020

Day 5: Binary Boarding
"""

from argparse import ArgumentParser
import logging
import re
import os
import sys

LOG = logging.getLogger(__name__)


def seats(fn):
    with open(fn) as fh:
        for raw_line in fh:
            line = raw_line.strip()
            yield line


TT = str.maketrans("FBLR", "0101")


def seats_id_iter():
    for seat in seats(r"..\day5_input.txt"):
        bin_seat = seat.translate(TT)
        seat_id = int(bin_seat, 2)
        yield seat_id


def part1():
    seat_ids = list()
    for seat in seats_id_iter():
        seat_ids.append(seat)
    LOG.info(f"{len(seat_ids)} seats, highest {max(seat_ids)}")


def part2():
    seat_ids = set()
    for seat in seats_id_iter():
        seat_ids.add(seat)
    all_seats = frozenset(list(range(min(seat_ids), max(seat_ids) + 1)))
    free_seats = all_seats.difference(seat_ids)
    LOG.info(f"{len(free_seats)} free seats")
    for x in free_seats:
        LOG.info(f"free {x}")
    

def cli(argv=None):
    # command line interface
    if argv is None:
        argv = sys.argv
    LOG.info("%s %s", os.path.basename(argv[0]), " ".join(argv[1:]))
    parser = ArgumentParser(description="Advent of code 2020")
    parser.add_argument("-1", "--part1", action='store_true')
    parser.add_argument("-2", "--part2", action='store_true')
    parser.add_argument("--showargs", action='store_true')
    parser.add_argument("--showenv", action='store_true')
    args = parser.parse_args(argv[1:])
    argd = vars(args)
    if args.showargs:
        # arguments
        for k, v in argd.items(): 
            print(k, v)
    if args.showenv:
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
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(process)i] %(levelname).4s %(module)s.%(funcName)s: %(message)s')
    sys.exit(cli())
