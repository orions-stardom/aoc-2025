#!/usr/bin/env python
import sys
from math import prod
from itertools import zip_longest, pairwise

def part_1(rawdata):
    *numeric_data, operations = rawdata.splitlines()
    numbers = [[int(i) for i in line.split()] for line in numeric_data]

    total = sum( (sum if op == "+" else prod)(num[i] for num in numbers) for i, op in enumerate(operations.split()))
    return str(total)

def part_2(rawdata):
    *numeric_data, operations = rawdata.splitlines()

    split_at = [0] + [i for i,chars in enumerate(zip_longest(*numeric_data, fillvalue=" ")) if all(c.isspace() for c in chars)] + [max(len(line) for line in numeric_data)]

    columnar = [[n[a:b] for n in numeric_data] for a,b in pairwise(split_at)]
    numbers = [[int("".join(c)) for c in zip(*column) if any(not x.isspace() for x in c) ] for column in columnar]

    total = sum((sum if op == "+" else prod)(nums) for op,nums in zip(operations.split(),numbers)) 
    return str(total)

from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
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
