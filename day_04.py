#!/usr/bin/env python
import sys

def parse(rawdata):
    return {x+1j*y:c  for y,line in enumerate(rawdata.splitlines()) for x,c in enumerate(line)}

def part_1(rawdata):
    grid = parse(rawdata)
    adjacencies = [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j]
    return str(sum(grid[pos] == "@" and sum(grid.get(pos+adj, ".") == "@" for adj in adjacencies) < 4 for pos in grid))

def part_2(rawdata):
    grid = parse(rawdata)
    adjacencies = [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j]
    cands = [pos for pos in grid if grid[pos] == "@" and sum(grid.get(pos+adj, ".") == "@" for adj in adjacencies) < 4]
    removed = 0
    while cands:
        for pos in cands:
            grid[pos] = "."
            removed += 1

        cands = [pos for pos in grid if grid[pos] == "@" and sum(grid.get(pos+adj, ".") == "@" for adj in adjacencies) < 4]

    return str(removed)

from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    # aoce parsing issue
    result = "13"
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    # aoce parsing issue
    # result = "43"
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
