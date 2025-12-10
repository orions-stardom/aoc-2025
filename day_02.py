#!/usr/bin/env python
import sys
import re

def buildrange(range_def):
    "'11-22' -> range(11,23)"
    lo,hi = range_def.split("-")
    return range(int(lo), int(hi)+1) # need to include hi


def part_1(rawdata):
    is_invalid = re.compile(r"(.+)\1").fullmatch
    return str(sum(id_ for range_def in rawdata.split(",") for id_ in buildrange(range_def) if is_invalid(str(id_))))

def part_2(rawdata):
    is_invalid = re.compile(r"(.+)\1+").fullmatch
    return str(sum(id_ for range_def in rawdata.split(",") for id_ in buildrange(range_def) if is_invalid(str(id_))))



from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    if result == "0":
        result = "1227775554"
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
