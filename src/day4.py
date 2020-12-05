#!python3
# Created 5 Dec 2020
# @author: andreas

""" Advent of code 2020

Day 4: Passport Processing  
"""

from argparse import ArgumentParser
import logging
import re
import os
import sys

LOG = logging.getLogger(__name__)


def read_passports(fn):
    pps = list()
    pp = dict()
    with open(fn) as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if len(line) > 0:
                kvs = line.split()
                for kv in kvs:
                    k, v = kv.split(':')
                    pp[k] = v
            else:
                LOG.debug(f"{pp}")
                pps.append(pp)
                pp = dict()
        if len(pp) > 0:
            LOG.debug(f"{pp}")
            pps.append(pp)
    LOG.info(f"{len(pps)} read")
    return pps


def part1():
    pps = read_passports(r"..\day4_input.txt")
    mandatory_tags = frozenset(('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid',))
    cnt = 0
    for pp in pps:
        pp_tags = set(pp.keys())
        LOG.debug(pp_tags)
        if mandatory_tags.issubset(pp_tags):
            cnt += 1
    LOG.info(f"{cnt}/{len(pps)} valid passport")

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
#     If cm, the number must be at least 150 and at most 193.
#     If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.


BYR_REO = re.compile("(\d{4})$")
HGTCM_REO = re.compile("(\d{3})cm")
HGTIN_REO = re.compile("(\d{2})in")
HCL_REO = re.compile("#(\d|[a-f]){6}$")
PID_REO = re.compile("(\d{9})$")


def part2():
    pps = read_passports(r"..\day4_input.txt")
    cnt = 0
    for pp in pps:
        LOG.debug(f"{pp}")
        valid_cnt = 0
        for tag, v in pp.items():
            if tag == "byr":
                if BYR_REO.match(v):
                    byr = int(v)
                    if byr >= 1920 and byr <= 2002:
                        valid_cnt += 1
            if tag == "iyr":
                if BYR_REO.match(v):
                    iyr = int(v)
                    if iyr >= 2010 and iyr <= 2020:
                        valid_cnt += 1
            if tag == "eyr":
                if BYR_REO.match(v):
                    eyr = int(v)
                    if eyr >= 2020 and eyr <= 2030:
                        valid_cnt += 1
            if tag == "hgt":
                if (mo := HGTCM_REO.match(v)):
                    hgt = int(mo[1])
                    if hgt >= 150 and hgt <= 193:
                        valid_cnt += 1
                if (mo := HGTIN_REO.match(v)):
                    hgt = int(mo[1])
                    if hgt >= 59 and hgt <= 76:
                        valid_cnt += 1
            if tag == "hcl":
                if HCL_REO.match(v):
                    valid_cnt += 1
            if tag == "ecl":
                if v in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
                    valid_cnt += 1
            if tag == "pid":
                if PID_REO.match(v):
                    valid_cnt += 1
        if valid_cnt == 7:
            cnt += 1
    LOG.info(f"{cnt}/{len(pps)} valid passport")


# alternative solution for part2 -----------------------------------

def passports(fn):
    with open(fn) as fh:
        fields = list()
        for raw_line in fh:
            line = raw_line.strip()
            if len(line) > 0:
                kvs = line.split()
                for kv in kvs:
                    fields.append(kv)
            else:
                yield fields
                fields = list()
        if len(fields) > 0:
            yield fields


checklist = (
    ('byr:(\d{4})$', 1920, 2002),
    ('iyr:(\d{4})$', 2010, 2020),
    ('eyr:(\d{4})$', 2020, 2030),
    ('hgt:(\d{3})cm$', 150, 193),
    ('hgt:(\d{2})in$', 59, 76),
    ('hcl:#(\d|[a-f]){6}$',),
    ('ecl:(amb|blu|brn|gry|grn|hzl|oth)$',),
    ('pid:(\d{9})$',),
    )


def part2b():
    cnt = 0
    for n, pp in enumerate(passports(r"..\day4_input.txt")):
        LOG.debug(f"{pp}")
        valid_cnt = 0
        for field in pp:
            for check in checklist:
                # LOG.debug(f"{field} for {check}")
                reo = re.compile(check[0])
                mo = reo.match(field)
                if mo:
                    if len(check) > 1:
                        v = int(mo[1])
                        if v >= check[1] and v <= check[2]:
                            valid_cnt += 1
                            break
                    else:
                        valid_cnt += 1
                        break
        if valid_cnt == 7:
            cnt += 1
    LOG.info(f"{cnt}/{n+1} valid passport")


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
        part2b()
    return 0


if __name__ == "__main__":
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s.%03d'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(process)i] %(levelname).4s %(module)s.%(funcName)s: %(message)s')
    sys.exit(cli())
