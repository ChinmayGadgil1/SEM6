def dfs(miss, cann, boat, visited=None, path=None):
    if visited is None:
        visited = []
    if path is None:
        path = []
    
    state = (miss, cann, boat)
    visited.append(state)
    path.append(state)

    if miss == 0 and cann == 0 and boat == 'R':
        print("\nSolution found!")
        for i, s in enumerate(path):
            print(f"{i}: {s}")
        return path

    if boat == 'L':
        next_states = [
            (miss-1, cann, 'R'), (miss-2, cann, 'R'),
            (miss-1, cann-1, 'R'), (miss, cann-1, 'R'),
            (miss, cann-2, 'R')
        ]
    else:
        next_states = [
            (miss+1, cann, 'L'), (miss+2, cann, 'L'),
            (miss+1, cann+1, 'L'), (miss, cann+1, 'L'),
            (miss, cann+2, 'L')
        ]

    for next_state in next_states:
        m, c, b = next_state
        if m < 0 or c < 0 or m > 3 or c > 3:
            continue
        if (m < c and m > 0) or (3-m < 3-c and 3-m > 0):
            continue
        if next_state not in visited:
            result = dfs(m, c, b, visited, path)
            if result:
                return result
    
    path.pop()
    return None

miss = int(input("Missionaries: "))
cann = int(input("Cannibals: "))
dfs(miss, cann, 'L')
