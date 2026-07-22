# ...existing code...
goal = ""
graph = {}
heuristics = {}
Nil = None
isAscending = False

def h(node):
    return heuristics.get(node, 99)

def ReconstructPath(nodepair, closed):
    path = [nodepair[0]]
    parent = nodepair[1]
    while parent is not Nil:
        path.append(parent)
        node = next((item for item in closed if item[0] == parent), Nil)
        parent = node[1] if node else Nil
    path.reverse()
    return path

def BestFirstSearch(start):
    open_list = [(start, Nil, h(start))]
    closed_list = []
    iteration = 1

    print("\nSimple Best-First Search trace:\n")
    while open_list:
        nodepair = open_list[0]
        node = nodepair[0]

        # simple display
        print(f"Iter {iteration} | OPEN: {[n[0] for n in open_list]} | CLOSED: {[n[0] for n in closed_list]}")

        if node == goal:
            return ReconstructPath(nodepair, closed_list)

        closed_list.insert(0, nodepair)
        children = graph.get(node, [])
        # remove seen
        seen = {item[0] for item in open_list} | {item[0] for item in closed_list}
        new_children = [c for c in children if c not in seen]
        # pair with parent and heuristic
        new_nodes = [(c, node, h(c)) for c in new_children]
        # prepend new nodes then sort by heuristic
        open_list = new_nodes + open_list[1:]
        open_list.sort(key=lambda x: x[2], reverse=isAscending)

        iteration += 1

    return None

def GetUserInput():
    global goal, graph, heuristics, isAscending
    n = int(input("Enter the number of nodes: "))

    for _ in range(n):
        name = input("\nNode: ").strip()
        val = int(input("Heuristic: "))
        children = input("Neighbors (space-separated): ").strip()
        heuristics[name] = val
        graph[name] = [ch for ch in children.split() if ch] if children else []

    start = input("\nEnter start node: ").strip()
    goal = input("Enter goal node: ").strip()

    if heuristics.get(start, 99) < heuristics.get(goal, 99):
        isAscending = True

    return start

start = GetUserInput()
path = BestFirstSearch(start)

if path:
    print(f"\nPath: {' -> '.join(path)}")
else:
    print("\nNo path found.")
