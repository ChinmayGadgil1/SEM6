def print_state(state):
    for i in range(3):
        print(" ".join(str(state[i*3+j]) if state[i*3+j] else "-" for j in range(3)))
    print()

def h(state, goal):
    return sum(1 for i, v in enumerate(state) if v != 0 and v != goal[i])

def get_moves(state):
    moves = []
    idx = state.index(0)
    row, col = divmod(idx, 3)
    
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_idx = nr * 3 + nc
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            moves.append(tuple(new_state))
    
    return moves

def steepest_descent(start, goal):
    node = start
    path = [node]
    visited = {node}
    iteration = 1
    
    print("8-Puzzle Steepest Descent\n")
    print_state(node)
    
    while True:
        neighbors = [n for n in get_moves(node) if n not in visited]
        
        if not neighbors:
            print(f"Local optimum at iteration {iteration}")
            return path
        
        best = min(neighbors, key=lambda x: h(x, goal))
        best_h = h(best, goal)
        
        if best_h >= h(node, goal):
            print(f"No improvement. Local optimum at iteration {iteration}")
            return path
        
        node = best
        path.append(node)
        visited.add(node)
        
        print(f"Iteration {iteration}:")
        print_state(node)
        
        if node == goal:
            print("Goal reached!")
            return path
        
        iteration += 1

def input_matrix(prompt):
    print(prompt)
    matrix = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        matrix.extend(row)
    return tuple(matrix)

start = input_matrix("Start state:")
goal = input_matrix("Goal state:")
steepest_descent(start, goal)
