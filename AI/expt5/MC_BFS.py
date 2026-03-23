from collections import deque

def bfs(miss, cann):
    visited = set()
    queue = deque([(miss, cann, 'L', [(miss, cann, 'L')])])
    visited.add((miss, cann, 'L'))
    
    while queue:
        curr_miss, curr_cann, boat, path = queue.popleft()
        
        if curr_miss == 0 and curr_cann == 0 and boat == 'R':
            print("\nSolution Path:")
            for i, s in enumerate(path):
                print(f"Step {i}: {s}")
            return path
        
        if boat == 'L':
            next_states = [
                (curr_miss-1, curr_cann, 'R'),
                (curr_miss-2, curr_cann, 'R'),
                (curr_miss-1, curr_cann-1, 'R'),
                (curr_miss, curr_cann-1, 'R'),
                (curr_miss, curr_cann-2, 'R')
            ]
        else:
            next_states = [
                (curr_miss+1, curr_cann, 'L'),
                (curr_miss+2, curr_cann, 'L'),
                (curr_miss+1, curr_cann+1, 'L'),
                (curr_miss, curr_cann+1, 'L'),
                (curr_miss, curr_cann+2, 'L')
            ]
        
        for next_state in next_states:
            m, c, b = next_state
            if m < 0 or c < 0 or m > 3 or c > 3:
                continue
            if m < c and m > 0:
                continue
            if 3-m < 3-c and 3-m > 0:
                continue
            if next_state not in visited:
                visited.add(next_state)
                queue.append((m, c, b, path + [next_state]))
    
    return None

miss = int(input("Enter no of missionaries: "))
cann = int(input("Enter no of cannibals: "))

result = bfs(miss, cann)
