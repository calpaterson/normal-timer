#!/usr/bin/python3

"""A timer program.

Runs another problem (arg 1) and then repeatedly passes it an input (arg 2)
while timing out long it took to respond.  When it's decided that it has enough
samples to make a judgement, it exits, printing it's final measurement (in
seconds).


"""

import statistics
from time import time
import sys
import subprocess


def is_normal(samples):
    # a normality test to drive any mathematician to drink
    if len(samples) < 100:
        return False
    mean = statistics.mean(samples)
    stddev = statistics.pstdev(samples)
    check = mean > stddev
    if len(samples) % 100 == 0:
        print("on sample %d; mean: %f, stddev: %f" % (len(samples), mean, stddev))
    return check


def main():
    process_parts = sys.argv[1].split(" ")
    inp = sys.argv[2] + "\n"

    proc = subprocess.Popen(
        process_parts,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    )
    samples = []
    while not is_normal(samples):
        start_time = time()
        proc.stdin.write(inp)
        proc.stdout.readline()
        end_time = time()
        samples.append(end_time - start_time)
    proc.terminate()
    print("%d samples total" % len(samples))
    print("%f seconds on average" % statistics.mean(samples))


if __name__ == "__main__":
    main()
