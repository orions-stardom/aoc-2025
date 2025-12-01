#!/usr/bin/env python
import sys
from itertools import accumulate
from collections import deque

def part_1(rawdata):
    data = [50] + [int(l[1:]) * (-1 if l.startswith("L") else 1) for l in rawdata.splitlines()]
    return str(sum(not s % 100 for s in accumulate(data)))

def part_2(rawdata):
    # Im sure theres a pure arithmetic way to do this but fuck it its day 1,
    # the numbers are probably small enough to just do it for real
    dial = deque(range(100))
    dial.rotate(50)

    zeroes = 0
    for l in rawdata.splitlines():
        num = int(l[1:])
        direction = -1 if l.startswith("L") else 1
        for _ in range(num):
            dial.rotate(direction)
            if dial[0] == 0:
                zeroes += 1

    return str(zeroes)


from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    if result == "50":
        # aoce parsing error
        result = "6"
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
