#!/usr/bin/env python
import sys
import itertools as it
import portion as P
from dataclasses import dataclass

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

def part_2(rawdata, debug=False):
    red_tiles = [coord(line) for line in rawdata.splitlines()]

    @dataclass
    class HorizontalLine:
        xs: P.Interval
        y: int

        def __contains__(self, point):
            return point.real in self.xs and point.imag == self.y

        def __str__(self):
            return f"({self.xs.lower}, {self.y})->({self.xs.upper}, {self.y})"

    @dataclass
    class VerticalLine:
        x: int
        ys: P.Interval 

        def __contains__(self, point):
            return point.real == self.x and point.imag in self.ys

        def __str__(self):
            return f"({self.x}, {self.ys.lower})->({self.x},{self.ys.upper})"


    verticals = []
    horizontals = []

    for p1,p2 in it.pairwise(red_tiles + [red_tiles[0]]):
        if p1.real == p2.real:
            verticals.append(VerticalLine(p1.real, P.open(min(p1.imag, p2.imag), max(p1.imag, p2.imag) )))
        elif p1.imag == p2.imag:
            horizontals.append(HorizontalLine(P.open(min(p1.real, p2.real), max(p1.real, p2.real) ), p1.imag))
        else:
            raise ValueError("Uh..")


    def point_in_polygon(z):
        inside = False
        for edge in verticals:
            if z in edge:
                return True

            if edge.x > z.real and  z.imag in edge.ys:
                inside = not inside

        return inside
    
    def valid_rectangle(a,b):
        xs = P.closed(min(a.real, b.real), max(a.real, b.real))
        ys = P.closed(min(a.imag, b.imag), max(a.imag, b.imag))

        corners = complex(xs.lower, ys.lower), \
                  complex(xs.upper, ys.lower), \
                  complex(xs.lower, ys.upper), \
                  complex(xs.upper, ys.upper)
        if not all(point_in_polygon(corner) for corner in corners):
            return False

        for line in verticals:
            if line.x in xs and (ys.lower in line.ys or ys.upper in line.ys):
                return False

        for line in horizontals:
            if (xs.lower in line.xs or xs.upper in line.xs) and line.y in ys:
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

    if debug:
        for y in range(max(int(z.imag) for z in red_tiles)+2):
            for x in range(max(int(z.real) for z in red_tiles)+2):
                z = complex(x,y)
                if z in best_ab:
                    print("[bold red]#[/bold red]", end="")
                elif z in {9+5j,2+3j}:
                    print("[bold blue]X[/bold blue]", end="")
                elif z in red_tiles:
                    print("[red]X[/red]", end="")
                elif any(z in line for line in horizontals+verticals):
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
    assert part_2(data, debug=True) == result

if __name__ == "__main__":
    res = pytest.main([__file__])
    if res:
        sys.exit(res.value)

    # part_2(puzzle.examples[0].input_data, debug=True)
    # part_2(puzzle.input_data)

    submit(part_1(puzzle.input_data), part="a", reopen=False)
    submit(part_2(puzzle.input_data), part="b", reopen=False)
