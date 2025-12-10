#!/usr/bin/env python
import sys
from collections import Counter

def part_1(rawdata):
    rows = rawdata.split()
    beams = {rows[0].index("S") }

    splitters_hit = 0
    for row in rows[1:]:
        next_beams = set()
        for beam in beams:
            if row[beam] == "^":
                next_beams |= {beam-1, beam+1}
                splitters_hit += 1
            else:
                next_beams.add(beam)

        beams = next_beams

    return str(splitters_hit )

def part_2(rawdata):
    rows = rawdata.split()
    beams = Counter({rows[0].index("S") })

    for row in rows[1:]:
        next_beams = Counter()
        for beam, count in beams.items():
            if row[beam] == "^":
                next_beams[beam-1] += count
                next_beams[beam+1] += count
            else:
                next_beams[beam] += count

        beams = next_beams

    return str(beams.total())

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
