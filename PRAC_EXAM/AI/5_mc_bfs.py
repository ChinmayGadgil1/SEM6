from collections import deque

def bfs(miss, cann):
    visited = set()
    parent = {}
    start = (miss, cann, 'L')
    queue = deque([start])
    visited.add(start)
    parent[start] = None

    while queue:
        curr = queue.popleft()
        m, c, b = curr

        if m == 0 and c == 0 and b == 'R':
            path = []
            s = curr
            while s is not None:
                path.append(s)
                s = parent[s]
            path.reverse()
            print("\nSolution:")
            for i, s in enumerate(path):
                print(f"{i}: {s}")
            return path

        if b == 'L':
            next_states = [
                (m-1, c, 'R'), (m-2, c, 'R'),
                (m-1, c-1, 'R'), (m, c-1, 'R'),
                (m, c-2, 'R')
            ]
        else:
            next_states = [
                (m+1, c, 'L'), (m+2, c, 'L'),
                (m+1, c+1, 'L'), (m, c+1, 'L'),
                (m, c+2, 'L')
            ]

        for nm, nc, nb in next_states:
            if nm < 0 or nc < 0 or nm > 3 or nc > 3:
                continue
            if (nm < nc and nm > 0) or (3-nm < 3-nc and 3-nm > 0):
                continue
            next_state = (nm, nc, nb)
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = curr
                queue.append(next_state)

    return None

miss = int(input("Missionaries: "))
cann = int(input("Cannibals: "))
bfs(miss, cann)
