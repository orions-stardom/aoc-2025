#!/usr/bin/env python
import sys
from itertools import accumulate, chain

def part_1(rawdata):
    data = [50] + [int(l.replace("R", "").replace("L","-")) for l in rawdata.splitlines()]
    return str(sum(not s % 100 for s in accumulate(data)))

def part_2(rawdata):
    data = [50] + list(chain.from_iterable([-1 if l.startswith("L") else 1]*int(l[1:]) for l in rawdata.splitlines()))
    return str(sum(not s % 100 for s in accumulate(data)))

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
