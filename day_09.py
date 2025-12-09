#!/usr/bin/env python
import sys
import itertools as it
import portion as P

from rich import print

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

        def __contains__(self, point):
            if self.vertical:
                return point.real == self.fixed and point.imag in self.interval
            else:
                return point.imag == self.fixed and point.real in self.interval

        def __str__(self):
            if self.vertical:
                return f"({self.fixed}, {self.interval.lower})->({self.fixed},{self.interval.upper})"
            else:
                return f"({self.interval.lower}, {self.fixed})->({self.interval.upper}, {self.fixed})"

    def polygon(points):
        poly = [Line(a,b) for a,b in it.pairwise(points)]
        poly.append(Line(points[0], points[-1]))
        return poly

    perimeter = polygon(red_tiles)

    def valid_rectangle(a,b):
        rectangle = polygon([a,complex(a.real,b.imag),b,complex(b.real,a.imag)])
        for l1, l2 in it.product(rectangle, perimeter):

            if l1.vertical == l2.vertical:
                if l1.fixed == l2.fixed and not l1.interval in l2.interval and not l2.interval in l1.interval:
                    return False 
                continue

            if l1.fixed in l2.interval and l2.fixed in l1.interval:
                return False

        return True

    # biggest = max(area(a,b) for a,b in it.combinations(red_tiles,2) if valid_rectangle(a,b)) 
    # the area calculation is considerably cheaper
    biggest = 0
    best_ab = ()
    for a,b in it.combinations(red_tiles,2):
        candidate = area(a,b)
        if candidate > biggest and valid_rectangle(a,b):
            biggest = candidate
            best_ab = a, b

    for y in range(max(int(z.imag) for z in red_tiles)+2):
        for x in range(max(int(z.real) for z in red_tiles)+2):
            z = complex(x,y)
            if z in best_ab:
                print("[bold red]#[/bold red]", end="")
            elif z in {9+5j,2+3j}:
                print("[bold blue]X[/bold blue]", end="")
            elif z in red_tiles:
                print("[red]X[/red]", end="")
            elif any(z in line for line in perimeter):
                print("[green]X[/green]", end="")
            else:
                print(".", end="")
        print()

    print()
    print("Area: ", biggest)

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
    # res = pytest.main([__file__])
    # if res:
    #     sys.exit(res.value)

    part_2(puzzle.examples[0].input_data)
    # part_2(puzzle.input_data)
    # submit(part_1(puzzle.input_data), part="a", reopen=False)
    # submit(part_2(puzzle.input_data), part="b", reopen=False)
