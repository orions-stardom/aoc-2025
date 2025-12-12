#!/usr/bin/env python
import sys
import re

from aocd import puzzle, submit

def part_1(rawdata):
    *shapedata, regiondata = rawdata.split("\n\n")
    shapes = [s.count("#") for s in shapedata]

    yeses = 0
    nos = 0
    maybes = 0
    for i, region in enumerate(regiondata.splitlines()):
        width,height,*counts = map(int, re.fullmatch(r"(\d+)x(\d+):(?:\s+(\d+)\s*)+", region).groups())
        area = width*height
                           
        require = sum(int(x) * shape for x,shape in zip(counts,shapes))
        
        if (width//3)*(height//3) >= sum(counts):
            yeses += 1
            result = "yes"
        elif area >= require:
            maybes += 1
            result = "maybe"
        else:
            nos += 1
            result = "no"

        # print(f"{require} / {area}  {int(require/area * 100)}% {result}")

    print("Yes:   ", yeses)
    print("No:    ", nos)
    print("Maybe: ", maybes)
    if not maybes:
        return str(yeses)

# no tests this time because the example has more baroque
# edge cases than the real thing

if __name__ == "__main__":
    submit(part_1(puzzle.input_data), part="a", reopen=False)
