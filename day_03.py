#!/usr/bin/env python
import sys
import itertools as it

def naive_max_joltage(bank, n):
    return max(int("".join(c)) for c in it.combinations(bank, n))

def smart_max_joltage(bank, n):
    max_so_far = 0
    bank = [int(b) for b in bank]
    for m in range(n, 0, -1):
        # Choose the maximum single joltage battery we can such that
        # there are still at least m-1 remaining to choose from
        cands = bank[:-m+1] if m > 1 else bank
        i, pick = max(enumerate(cands), key=lambda ix: ix[1])
        bank = bank[i+1:]
        assert len(bank) >= m-1
        max_so_far = 10*max_so_far + pick

    return max_so_far

def part_1(rawdata):
    banks = [list(l) for l in rawdata.splitlines()]
    return str(sum(naive_max_joltage(bank, 2) for bank in banks))

def part_2(rawdata):
    banks = [list(l) for l in rawdata.splitlines()]
    # return str(sum(naive_max_joltage(bank, 12) for bank in banks))
    return str(sum(smart_max_joltage(bank, 12) for bank in banks))

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
