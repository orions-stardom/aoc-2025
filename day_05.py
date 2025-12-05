#!/usr/bin/env python
import sys
import portion as P

def inclusive_range(data):
    lo,hi = data.split("-")
    return range(int(lo), int(hi)+1)

def part_1(rawdata):
    range_data, ingredient_data = rawdata.split("\n\n")
    ranges = [inclusive_range(line) for line in range_data.splitlines()]
    ingredients = [int(l) for l in ingredient_data.splitlines()]

    return str(sum(any(i in r for r in ranges) for i in ingredients)) 

def part_2(rawdata):
    range_data, _ = rawdata.split("\n\n")
    ingredients = P.empty()
    for r in range_data.splitlines():
        lo, hi = r.split("-")
        ingredients |= P.closed(int(lo),int(hi))

    n_ingredients = sum(p.upper-p.lower+1 for p in ingredients)
    return str(n_ingredients)


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

    # submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
