#!/usr/bin/env python
import sys
import itertools as it
import portion as P

def coord(data):
    a,b = data.split(",")
    return complex(int(a), int(b))

def area(a,b):
    dx = abs(a.real-b.real)+1
    dy = abs(a.imag-b.imag)+1
    return int(dx*dy)

def part_1(rawdata):
    coords = [coord(line) for line in rawdata.splitlines()]

    biggest = max(area(a,b) for a,b in it.combinations(coords,2) )
    return str(biggest)

def part_2(rawdata):
    red_tiles = [coord(line) for line in rawdata.splitlines()]

    class Line:
        def __init__(self, a,b):
            if a.real == b.real:
                self.vertical = True
                self.fixed = a.real
                self.interval = P.open(min(a.imag,b.imag), max(a.imag, b.imag))
            elif a.imag == b.imag:
                self.vertical = False 
                self.fixed = a.imag
                self.interval = P.open(min(a.real,b.real), max(a.real, b.real))
            else:
                raise ValueError("only horizontal and vertical lines exist")

    def polygon(points):
        poly = [Line(a,b) for a,b in it.pairwise(points)]
        poly.append(Line(points[0], points[-1]))
        return poly

    def lines_intersect(l1, l2):
        if l1.vertical == l2.vertical:
            return False

        return l1.fixed in l2.interval and l2.fixed in l1.interval

    def polygons_intersect(poly1, poly2):
        return any(lines_intersect(l1,l2) for l1,l2 in it.product(poly1, poly2))

    perimeter = polygon(red_tiles)

    def valid_rectangle(a,b):
        rectangle = polygon([a,complex(a.real,b.imag),b,complex(b.real,a.imag)])
        return not polygons_intersect(perimeter,rectangle)

    # biggest = max(area(a,b) for a,b in it.combinations(red_tiles,2) if valid_rectangle(a,b)) 
    # the area calculation is considerably cheaper
    biggest = 0
    for a,b in it.combinations(red_tiles,2):
        candidate = area(a,b)
        if candidate > biggest and valid_rectangle(a,b):
            biggest = candidate

    return str(biggest)
        
from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    result = "50" # aoce parsing error
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    result = "24" # more aoce parsing error
    assert part_2(data) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
