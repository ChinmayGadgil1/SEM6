def print_matrix(state):
    for i in range(3):
        print(" ".join(str(state[i*3 + j]) if state[i*3 + j] != 0 else "-" for j in range(3)))
    print()

def GoalTest(node):
    return node == goal

def MoveGen(node):
    moves = []
    state = list(node)
    zero_pos = state.index(0)
    row, col = divmod(zero_pos, 3)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_pos = new_row * 3 + new_col
            new_state = state[:]
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            moves.append(tuple(new_state))
    
    return moves

def h(node):
    count = 0
    for i, val in enumerate(node):
        if val != 0 and val == goal[i]:
            count += 1
    return 8 - count  

def SteepestDescent(start):
    node = start
    path = [node]
    visited = {node}
    iteration = 1


    while True:
        neighbors = [n for n in MoveGen(node) if n not in visited]

        if not neighbors:
            print(f"{iteration:<6} {str(node):<15} STOP")
            return path

        neighbor_pairs = [(n, h(n)) for n in neighbors]
        
        print(f"\nIteration {iteration}:")
        for idx, (neighbor, h_val) in enumerate(neighbor_pairs, 1):
            print(f"{idx}: {neighbor} h={h_val}")
        
        best_node, best_h = min(neighbor_pairs, key=lambda x: x[1])
        print(f"chosen: {best_node} h={best_h}\n")

        if best_h >= h(node):
            print("Local optimum reached")
            return path

        node = best_node
        path.append(node)
        visited.add(node)

        if GoalTest(node):
            return path

        iteration += 1

def InputMatrix(prompt):
    print(prompt)
    matrix = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        matrix.extend(row)
    return tuple(matrix)

start = InputMatrix("Enter start state:")
goal = InputMatrix("Enter goal state:")

path = SteepestDescent(start)

if path:
    print(f"\nPath length: {len(path)}")
    for i, state in enumerate(path):
        print(f"Step {i}:")
        print_matrix(state)
else:
    print("\nNo path found.")