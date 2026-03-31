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

def Head(lst):
    return lst[0] if lst else None

def Tail(lst):
    return lst[1:] if lst else []

def Cons(item, lst):
    return [item] + lst

def Append(lst1, lst2):
    return lst1 + lst2

def RemoveSeen(children, open_list, closed_list):
    seen = [item[0] for item in open_list] + [item[0] for item in closed_list]
    return [k for k in children if k not in seen]

def MakePairs(children, parent):
    return [(child, parent, h(child)) for child in children]

def Sort_h(lst):
    return sorted(lst, key=lambda x: x[2])

def ReconstructPath(nodepair, closed_list):
    path = [nodepair[0]]
    parent = nodepair[1]
    while parent is not None:
        path.append(parent)
        node = next((item for item in closed_list if item[0] == parent), None)
        parent = node[1] if node else None
    path.reverse()
    return path

def FormatLine(lst, width=60):
    s = str([(n, str(p)[:10] if p else "Nil", hv) for n, p, hv in lst]).replace("None", "Nil")
    if len(s) <= width:
        return [s]
    lines = []
    current = "["
    items = [str(item).replace("None", "Nil") for item in lst]
    for i, item_str in enumerate(items):
        suffix = ", " if i < len(items) - 1 else "]"
        combined = item_str + suffix
        if len(current + combined) > width and current != "[":
            lines.append(current)
            current = " " + combined
        else:
            current += combined
    lines.append(current)
    return lines

def BestFirstSearch(start):
    open_list  = [(start, None, h(start))]
    closed_list = []
    iteration = 1

    print(f"\n{'':>4} {'OPEN':<55} CLOSED")

    while open_list:
        nodepair = Head(open_list)
        node     = nodepair[0]

        open_lines   = FormatLine(open_list)
        closed_lines = FormatLine(closed_list)
        max_idx = max(len(open_lines), len(closed_lines))

        for i in range(max_idx):
            prefix = f"{iteration}: " if i == 0 else "   "
            o_text = open_lines[i]   if i < len(open_lines)   else ""
            c_text = closed_lines[i] if i < len(closed_lines) else ""
            print(f"{prefix:<4} {o_text:<60} {c_text}")

        if GoalTest(node):
            return ReconstructPath(nodepair, closed_list)

        closed_list = Cons(nodepair, closed_list)
        children    = MoveGen(node)
        noLoops     = RemoveSeen(children, open_list, closed_list)
        new_nodes   = MakePairs(noLoops, node)
        open_list   = Sort_h(Append(new_nodes, Tail(open_list)))
        iteration  += 1
        print()

    return None

def InputMatrix(prompt):
    print(prompt)
    matrix = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        matrix.extend(row)
    return tuple(matrix)

start = InputMatrix("Enter start state:")
goal  = InputMatrix("Enter goal state:")

path = BestFirstSearch(start)

if path:
    print(f"\nPath length: {len(path)}")
    for i, state in enumerate(path):
        print(f"Step {i}:")
        print_matrix(state)
else:
    print("\nNo path found.")