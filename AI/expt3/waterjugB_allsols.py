from math import gcd
from collections import deque

def is_possible(jug1_cap, jug2_cap, target):
    if target > max(jug1_cap, jug2_cap):
        return False
    if target % gcd(jug1_cap, jug2_cap) != 0:
        return False
    return True

def bfs_all_solutions(start, target, jug1_cap, jug2_cap):
    visited = set()
    queue = deque()

    queue.append([start])  
    visited.add(start)

    solutions = []

    while queue:
        path = queue.popleft()
        jug1, jug2 = path[-1]

        if jug1 == target or jug2 == target:
            solutions.append(path)
            continue

        next_states = [
            (jug1_cap, jug2),
            (jug1, jug2_cap),
            (0, jug2),
            (jug1, 0),

            (jug1 - min(jug1, jug2_cap - jug2),
             jug2 + min(jug1, jug2_cap - jug2)),

            (jug1 + min(jug2, jug1_cap - jug1),
             jug2 - min(jug2, jug1_cap - jug1))
        ]

        for state in next_states:
            if state not in visited:
                visited.add(state)
                queue.append(path + [state])

    return solutions


jug1_cap = int(input("Enter capacity of jug1: "))
jug2_cap = int(input("Enter capacity of jug2: "))
target = int(input("Enter required amount: "))

if is_possible(jug1_cap, jug2_cap, target):
    solutions = bfs_all_solutions((0,0), target, jug1_cap, jug2_cap)

    print(f"\nFound {len(solutions)} solution(s):\n")

    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i}:")
        for step, state in enumerate(sol):
            print(f" Step {step}: {state}")
        print()
else:
    print("No solution possible")
