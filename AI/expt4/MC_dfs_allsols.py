def dfs(miss, cann, boat, visited=None, path=None,all_solutions=None):
    if visited is None:
        visited = []
    if path is None:
        path = []
    if all_solutions is None:
        all_solutions = []
    
    state = (miss, cann, boat)
    visited.append(state)
    path.append(state)

    if miss == 0 and cann == 0 and boat == 'R':
        print("\nSolution Path:")
        all_solutions.append(list(path))
        for i, s in enumerate(path):
            print(f"Step {i}: {s}")
        path.pop()
        visited.remove(state)
        return all_solutions

    
    if boat == 'L':
        next_states = [
            (miss-1, cann, 'R'),
            (miss-2, cann, 'R'),
            (miss-1, cann-1, 'R'),
            (miss, cann-1, 'R'),
            (miss, cann-2, 'R')
        ]
        for next_state in next_states:
            if next_state[0] < 0 or next_state[1] < 0:
                continue
            if next_state[0] < next_state[1] and next_state[0] > 0:
                continue
            if 3-next_state[0] < 3-next_state[1] and 3-next_state[0] > 0:
                continue
            if next_state not in visited:
                dfs(next_state[0], next_state[1], next_state[2], visited, path,all_solutions)
                
    else:
        next_states = [
            (miss+1, cann, 'L'),
            (miss+2, cann, 'L'),
            (miss+1, cann+1, 'L'),
            (miss, cann+1, 'L'),
            (miss, cann+2, 'L')
        ]
        for next_state in next_states:
            if next_state[0] > 3 or next_state[1] > 3:
                continue
            if next_state[0] < next_state[1] and next_state[0] > 0:
                continue
            if 3-next_state[0] < 3-next_state[1] and 3-next_state[0] > 0:
                continue
            if next_state not in visited:
                dfs(next_state[0], next_state[1], next_state[2], visited, path,all_solutions)
                
    path.pop()
    return all_solutions

miss = int(input("Enter no of missionaries: "))
cann = int(input("Enter no of cannibals: "))

solutions = dfs( miss,cann,'L')
if solutions:
    print(f"\nFound {len(solutions)} solution:\n")
    for i, solution in enumerate(solutions, 1):
            print(f"Solution {i}: {' -> '.join(map(str, solution))}")
else:
    print("\nNo solution found.")


