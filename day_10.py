#!/usr/bin/env python
import sys
from itertools import accumulate, chain
import ast
from collections import deque

from scipy.optimize import linprog

def solve_lights(machine):
    light_data, *switch_data, _ = machine.split()
    target = int(light_data[1:-1][::-1].replace("#","1").replace(".","0"), 2)
    
    def switchify(n):
        if isinstance(n, int):
            return 1 << n

        ret = 0
        for nn in n:
            ret |= (1 << nn)

        return ret

    switches = [switchify(ast.literal_eval(d)) for d in switch_data]
    q = deque([ (0, 0) ])
    seen = set()
    while q:
        steps, state = q.popleft()
        if state == target:
            return steps
        if state in seen:
            continue
        seen.add(state)

        q.extend((steps+1, state^switch) for switch in switches)

    raise ValueError("uhh..")

def solve_joltage(machine):
    _, *switch_data, joltage_data = machine.split()
    target = ast.literal_eval(joltage_data[1:-1])
    switches = [ [i in ast.literal_eval(f"[{s[1:-1]}]") for i in range(len(target))] for s in switch_data]

    # https://en.wikipedia.org/wiki/Integer_programming
    # This will find minimum vector x subject to: switches @ x = target
    # the mandatory coefficients vector is all 1s in this case since the switches
    # are equally weighted
    # So the matrix equation represents the act of pressing each switch_n `x_n` times
    # which .. is just directly what we need
    # integrality=1 means x must have only integer entries, which is the "no half presses" constraint
    # from the problem

    sol = linprog([1] * len(switches), A_eq=list(zip(*switches)), b_eq=target, integrality=1)
    # sol.x has the number of times to press each button, but sol.fun conveniently adds them all up for us
    return int(sol.fun)

def part_1(rawdata):
    return str(sum(solve_lights(machine) for machine in rawdata.splitlines()))

def part_2(rawdata):
    return str(sum(solve_joltage(machine) for machine in rawdata.splitlines()))

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
