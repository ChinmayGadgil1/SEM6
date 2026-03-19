

def dfs(miss, cann, boat, visited=None, path=None):
    if visited is None:
        visited = []
    if path is None:
        path = []
    
    state = (miss, cann, boat)
    visited.append(state)
    path.append(state)

    if miss == 0 and cann == 0 and boat == 'R':
        print("\nSolution Path:")
        for i, s in enumerate(path):
            print(f"Step {i}: {s}")
        return path

    
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
                result = dfs(next_state[0], next_state[1], next_state[2], visited, path)
                if result:
                    return result
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
                result = dfs(next_state[0], next_state[1], next_state[2], visited, path)
                if result:
                    return result
    path.pop()
    return None

miss = int(input("Enter no of missionaries: "))
cann = int(input("Enter no of cannibals: "))

result = dfs(miss, cann, 'L')

