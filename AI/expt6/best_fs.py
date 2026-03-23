goal = ""
graph = {}
heuristics = {}
Nil = None
isAscending = False

def Head(list):
    return list[0] if list else None

def Tail(list):
    return list[1:] if list else []

def Cons(item, list):
    return [item] + list

def Append(list1, list2):
    return list1 + list2

def GoalTest(node):
    return node == goal

def MoveGen(node):
    return graph.get(node, [])

def h(node):
    return heuristics.get(node, 99)

def RemoveSeen(children, open, closed):
    seen = [item[0] for item in open] + [item[0] for item in closed]
    return [k for k in children if k not in seen]

def MakePairs(list, node):
    return [(k, node, h(k)) for k in list]

def Sort_h(list):
    return sorted(list, key=lambda x: x[2], reverse=isAscending)

def ReconstructPath(nodepair, closed):
    path = [nodepair[0]]
    parent = nodepair[1]
    while parent is not Nil:
        path.append(parent)
        node = next((item for item in closed if item[0] == parent), Nil)
        parent = node[1] if node else Nil
    path.reverse()
    return path

def FormatLine(list_obj, width=50):
    s = str(list_obj).replace("None", "Nil")
    if len(s) <= width:
        return [s]
    
    lines = []
    items = [str(item).replace("None", "Nil") for item in list_obj]
    
    current = "["
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
    open_list = [(start, Nil, h(start))]
    closed_list = []
    iteration = 1

    print(f"\n{' ':<15} OPEN {' ':<45} CLOSED")

    while open_list:
        nodepair = Head(open_list)
        node = nodepair[0]

        open_lines = FormatLine(open_list)
        closed_lines = FormatLine(closed_list)
        max_idx = max(len(open_lines), len(closed_lines))

        for i in range(max_idx):
            prefix = f"{iteration}: " if i == 0 else "   "
            o_text = open_lines[i] if i < len(open_lines) else ""
            c_text = closed_lines[i] if i < len(closed_lines) else ""
            print(f"{prefix:<4} {o_text:<55} {c_text}")

        if GoalTest(node):
            return ReconstructPath(nodepair, closed_list)
        else:
            closed_list = Cons(nodepair, closed_list)
            children = MoveGen(node)
            noLoops = RemoveSeen(children, open_list, closed_list)
            new_nodes = MakePairs(noLoops, node)
            open_list = Sort_h(Append(new_nodes, Tail(open_list)))
            iteration += 1
            print()
    
    return None

def GetUserInput():
    global goal, graph, heuristics, isAscending
    n = int(input("Enter the number of nodes: "))

    for _ in range(n):
        name = input("\nNode: ")
        val = int(input(f"Heuristics: "))
        children = input(f"Neighbors: ")
        heuristics[name] = val
        graph[name] = [n.strip() for n in children.split(' ')] if children else []

    start = input("\nEnter start node: ")
    goal = input("Enter goal node: ")
    
    if (heuristics[start] < heuristics[goal]):
        isAscending = True

    return start

start = GetUserInput()
path = BestFirstSearch(start)

if path:
    print(f"\nPath: {' -> '.join(path)}")
else:
    print("\nNo path found.")