from math import gcd

def is_possible(jug1_cap, jug2_cap, target):
    if target > max(jug1_cap, jug2_cap):
        return False
    if target % gcd(jug1_cap, jug2_cap) != 0:
        return False
    return True

def dfs(state, target, jug1_cap, jug2_cap, visited=None, parent=None):
    if visited is None:
        visited = []
    
    visited.append(state)
    print(state, end=" ")
    
    jug1, jug2 = state
    if jug1 == target or jug2 == target:
        print(f"\n\nTarget {target} liters achieved!")
        return visited

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
        if next_state == parent:
            continue
        if next_state not in visited:
            result = dfs(next_state, target, jug1_cap, jug2_cap, visited, state)
            if result:
                return result
    
    return None

jug1_cap = int(input("Enter capacity of jug1: "))
jug2_cap = int(input("Enter capacity of jug2: "))
target = int(input("Enter required amount: "))

if is_possible(jug1_cap, jug2_cap, target):
    print("DFS Traversal: ", end="")
    start = (0, 0)
    result = dfs(start, target, jug1_cap, jug2_cap)
    if not result:
        print("\nNo solution found.")
else:
    print("\nInvalid input.")

