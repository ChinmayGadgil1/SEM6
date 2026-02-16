from math import gcd

def is_possible(jug1_cap, jug2_cap, target):
    if target > max(jug1_cap, jug2_cap):
        return False
    if target % gcd(jug1_cap, jug2_cap) != 0:
        return False
    return True

def dfs(state, target, jug1_cap, jug2_cap, path=None, visited=None, all_solutions=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()
    if all_solutions is None:
        all_solutions = []
    
    path.append(state)
    visited.add(state)
    
    jug1, jug2 = state
    if jug1 == target or jug2 == target:
        all_solutions.append(list(path))
        path.pop()
        visited.remove(state)
        return all_solutions

    next_states = [
        (jug1_cap, jug2),
        (jug1, jug2_cap), 
        (0, jug2), 
        (jug1, 0), 
        (jug1 - min(jug1, jug2_cap - jug2), jug2 + min(jug1, jug2_cap - jug2)), 
        (jug1 + min(jug2, jug1_cap - jug1), jug2 - min(jug2, jug1_cap - jug1))   
    ]
    
    for next_state in next_states:
        if next_state[0] < 0 or next_state[1] < 0:
            continue
        if next_state[0] > jug1_cap or next_state[1] > jug2_cap:
            continue
        if next_state not in visited:
            dfs(next_state, target, jug1_cap, jug2_cap, path, visited, all_solutions)
    
    path.pop()
    visited.remove(state)
    return all_solutions

jug1_cap = int(input("Enter capacity of jug1: "))
jug2_cap = int(input("Enter capacity of jug2: "))
target = int(input("Enter required amount: "))

if is_possible(jug1_cap, jug2_cap, target):
    start = (0, 0)
    solutions = dfs(start, target, jug1_cap, jug2_cap)
    if solutions:
        print(f"\nFound {len(solutions)} solution:\n")
        for i, solution in enumerate(solutions, 1):
            print(f"Solution {i}: {' -> '.join(map(str, solution))}")
    else:
        print("\nNo solution found.")
else:
    print("\nInvalid input.")
