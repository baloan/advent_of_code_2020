#!python3
# Created 5 Dec 2020
# @author: andreas

""" Advent of code 2020

Day 6: Custom Customs
"""

from argparse import ArgumentParser
import logging
import os
import sys

LOG = logging.getLogger(__name__)


def lines(fn):
    with open(fn) as fh:
        for raw_line in fh:
            line = raw_line.strip()
            yield line


def answer_union():
    group = set()
    for line in lines(r"..\day6_input.txt"):
        if len(line) > 0:
            for c in line:
                group.add(c)
        else:
            yield group
            group = set()
    if len(group) > 0:
        yield group


def part1():
    yes_cnt = 0
    for group in answer_union():
        yes_cnt += len(group)
    LOG.info(f"{yes_cnt} answer_union")


def answer_intersection():
    users = list()
    for line in lines(r"..\day6_input.txt"):
        if len(line) > 0:
            user = set()
            for c in line:
                user.add(c)
            users.append(user)
        else:
            for user in users:
                print(",".join(user))
            everyone_yes = set.intersection(*users)
            print("+++++++++++++")
            print(",".join(everyone_yes))
            yield everyone_yes
            users = list()
            print("-------------")
    if len(users) > 0:
        everyone_yes = set.intersection(*users)
        yield everyone_yes


def part2():
    yes_cnt = 0
    for group in answer_intersection():
        yes_cnt += len(group)
    LOG.info(f"{yes_cnt} answer_intersection")
    

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
    if args.part1 or not args.part2:
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
