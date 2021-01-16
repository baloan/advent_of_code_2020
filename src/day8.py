#!python3
# Created 5 Dec 2020
# @author: andreas

""" Advent of code 2020

Day 8: Handheld Halting
"""

from argparse import ArgumentParser
import logging
import re
import os
import sys

LOG = logging.getLogger(__name__)


class AbsConsole():
    """ Abstract base class of console """

    def __init__(self):
        self.reset()
        self.opcode_lut = {
            "jmp": self.jmp,
            "nop": self.nop,
            "acc": self.acc,
            }
        
    def reset(self, program=None):
        self.accumulator = 0
        self.program_counter = 0
        self.program = program
        self.prev_pc = dict()
    
    def load_program(self, fn):
        prg = list()
        with open(fn) as fh:
            for raw_line in fh:
                line = raw_line.strip()
                opcode, args = line.split()
                arg = int(args)
                prg.append((opcode, arg))
        self.program = prg

    def run(self):
        raise NotImplementedError()

    def jmp(self, n):
        self.program_counter += n
        
    def nop(self, n):
        self.program_counter += 1
        
    def acc(self, n):
        self.accumulator += n
        self.program_counter += 1


class LoopConsole(AbsConsole):

    def __init__(self):
        super().__init__()
    
    def run(self):
        while(True):
            opcode, arg = self.program[self.program_counter]
            LOG.debug(f"{self.program_counter:04} {opcode} {arg}: {self.accumulator}")
            self.prev_pc[self.program_counter] = self.accumulator
            self.opcode_lut[opcode](arg)
            if self.program_counter in self.prev_pc:
                LOG.info(f"LOOP! {self.program_counter:04} {opcode} {arg}: {self.accumulator}, {self.prev_pc[self.program_counter]}")
                return self.prev_pc[self.program_counter]


def part1():
    con = LoopConsole()
    con.load_program(r"..\day8_input.txt")
    acc = con.run()
    LOG.info(f"acc is {acc} before loop")


class EndConsole(AbsConsole):

    def __init__(self):
        super().__init__()
    
    def run(self):
        while(True):
            opcode, arg = self.program[self.program_counter]
            # LOG.debug(f"{self.program_counter:04} {opcode} {arg}: {self.accumulator}")
            self.prev_pc[self.program_counter] = self.accumulator
            self.opcode_lut[opcode](arg)
            if self.program_counter in self.prev_pc:
                raise Exception()
            if self.program_counter == len(self.program):
                LOG.info(f"End program.")
                return self.accumulator


def mutations(program):
    for n, instruction in enumerate(program):
        opcode, arg = instruction 
        if opcode == "jmp":
            mutation = program[:]
            mutation[n] = ("nop", arg)
            LOG.debug(f"{n:04} {opcode} {arg}: mutate")
            yield mutation
        elif opcode == "nop":
            mutation = program[:]
            mutation[n] = ("jmp", arg)
            LOG.debug(f"{n:04} {opcode} {arg}: mutate")
            yield mutation


def part2():
    org = EndConsole()
    org.load_program(r"..\day8_input.txt")
    for mutation in mutations(org.program):
        life = EndConsole()
        life.reset(mutation)
        try:
            acc = life.run()
            LOG.info(f"acc is {acc} after loop")
            break
        except:
            LOG.info(f"mutation failed")
    

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
