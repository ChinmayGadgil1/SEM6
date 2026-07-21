def dfs(x, y, goal_x, goal_y, visited=None, path=None):
    if visited is None:
        visited = []
    if path is None:
        path = []
    
    state = (x, y)
    visited.append(state)
    path.append(state)

    if state == (goal_x, goal_y):
        print("\nSolution:")
        for i, s in enumerate(path):
            print(f"{i}: {s}")
        return path

    next_states = [
        (5, y),      # Fill jug1
        (x, 3),      # Fill jug2
        (0, y),      # Empty jug1
        (x, 0),      # Empty jug2
        (min(5, x + y), max(0, y - (5 - x))),  # Pour jug2 to jug1
        (max(0, x - (3 - y)), min(3, x + y))   # Pour jug1 to jug2
    ]

    for nx, ny in next_states:
        if (nx, ny) not in visited and (nx, ny) not in [(s[0], s[1]) for s in path]:
            result = dfs(nx, ny, goal_x, goal_y, visited, path)
            if result:
                return result
    
    path.pop()
    return None

print("Water Jug Problem")
goal_x = int(input("Goal X: "))
goal_y = int(input("Goal Y: "))
dfs(0, 0, goal_x, goal_y)
