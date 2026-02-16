from math import gcd
from collections import deque

def is_possible(jug1_cap, jug2_cap, target):
    if target % gcd(jug1_cap, jug2_cap) != 0:
        return False
    return True

def bfs(start, target, jug1_cap, jug2_cap):
    visited = []
    parent = {}
    queue = deque()
    
    queue.append(start)
    visited.append(start)
    parent[start] = None
    
    while queue:
        jug1, jug2 = queue.popleft()
        
        if jug1 == target or jug2 == target:
            path = []
            current = (jug1, jug2)
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            
            print("\nSolution Path:")
            for i, state in enumerate(path):
                print(f"Step {i}: {state}")
            
            return path
        
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
            if state[0] < 0 or state[1] < 0:
                continue
            if state[0] > jug1_cap or state[1] > jug2_cap:
                continue
            if state not in visited:
                visited.append(state)
                parent[state] = (jug1, jug2)
                queue.append(state)
    
    return None



jug1_cap = int(input("Enter capacity of jug1: "))
jug2_cap = int(input("Enter capacity of jug2: "))
target = int(input("Enter required amount: "))

if(target < 0 or jug1_cap < 0 or jug2_cap < 0 or target > max(jug1_cap, jug2_cap)):
    print("\nInvalid input.")
    

if is_possible(jug1_cap, jug2_cap, target):
    start = (0, 0)
    result = bfs(start, target, jug1_cap, jug2_cap)
    if not result:
        print("\nNo solution found.")
else:
    print("\nSolution not possible.")
