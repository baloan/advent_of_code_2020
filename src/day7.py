#!python3
# Created 5 Dec 2020
# @author: andreas

""" Advent of code 2020

Day 7: Handy Haversacks
"""

from argparse import ArgumentParser
import logging
import re
import os
import sys
from pprint import pprint

LOG = logging.getLogger(__name__)

ROOT_REO = re.compile(r"(\w*\s\w*) bags contain(.*)")
LEAF_REO = re.compile(r" (\d+) (\w+\s\w+) bags?[.]?")


def recurse_parents(bag_pairs, path, paths):
    leaf = path[-1]
    LOG.debug(f"level {len(path)}, paths {len(paths)}")
    for parent, child in bag_pairs:
        if child == leaf:
            subpath = path[:]
            subpath.append(parent)
            LOG.debug(f'path added {"/".join(subpath)}')
            paths.add(parent)
            paths = recurse_parents(bag_pairs, subpath, paths)
    return paths


def part1():
    lines = open(f"..\day7_input.txt", "r").readlines() 
    bag_pairs = list()
    for line in lines:
        mo = ROOT_REO.match(line)
        if mo: 
            parent = mo.group(1)
            children = mo.group(2).split(",")
            for part in children:
                mo2 = LEAF_REO.match(part)
                if mo2:
                    num = mo2.group(1)
                    child = mo2.group(2)
                    bag_pairs.append((parent, child))
                else:
                    LOG.warning(f"<{part}>")
        else:
            LOG.warning(line)
    # path builder
    pprint(bag_pairs)
    paths = recurse_parents(bag_pairs, ["shiny gold", ], set())
    LOG.info(f"colors {len(paths)}")


def recurse_children(bag_pairs, path):
    leaf = path[-1]
    children = False
    subtreecnt = 0
    for parent, num, child in bag_pairs:
        if parent == leaf:
            children = True
            subpath = path[:]
            subpath.append(child)
            subcnt = recurse_children(bag_pairs, subpath)
            subtreecnt += subcnt * int(num)
            LOG.debug(f'    path /{"/".join(subpath)}$ returns {subtreecnt} = {num} * {subcnt}')
    if not children:
        LOG.debug(f'endpoint /{"/".join(path)}$')
        subtreecnt = 1
    return subtreecnt


def part2():
    lines = open(f"..\day7_input.txt", "r").readlines() 
    bag_pairs = list()
    for line in lines:
        mo = ROOT_REO.match(line)
        if mo: 
            parent = mo.group(1)
            children = mo.group(2).split(",")
            for part in children:
                mo2 = LEAF_REO.match(part)
                if mo2:
                    num = mo2.group(1)
                    child = mo2.group(2)
                    bag_pairs.append((parent, num, child))
                else:
                    LOG.warning(f"<{part}>")
        else:
            LOG.warning(line)
    # path builder
    pprint(bag_pairs)
    bag_count = recurse_children(bag_pairs, ["shiny gold", ])
    LOG.info(f"bags {bag_count}")
    

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
