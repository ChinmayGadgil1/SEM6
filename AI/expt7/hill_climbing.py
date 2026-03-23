goal = ""
graph = {}
heuristics = {}
isAscending = False

def GoalTest(node):
    return node == goal

def MoveGen(node):
    return graph.get(node, [])

def h(node):
    return heuristics.get(node, 99)

def HillClimbing(start):
    node = start
    path = [node]
    visited = set([node])
    iteration = 1

    print(f"\n{'Iter':<6} {'Current':<10} {'Neighbors (h)':<35} {'Chosen':<10}")

    while True:
        neighbors = [n for n in MoveGen(node) if n not in visited]

        if not neighbors:
            print(f"{iteration:<6} {node:<10} {'[]':<35} {'STOP'}")
            return path

        neighbor_pairs = [(n, h(n)) for n in neighbors]

        chosen = None

        for n in neighbors:
            if (isAscending and h(n) > h(node)) or (not isAscending and h(n) < h(node)):
                chosen = n
                break

        print(f"{iteration:<6} {node:<10} {str(neighbor_pairs):<35} {chosen if chosen else 'None'}")

        if chosen is None:
            print("\nNo better neighbor → Stuck at Local Optimum")
            return path

        node = chosen
        path.append(node)
        visited.add(node)

        if GoalTest(node):
            return path

        iteration += 1

def GetUserInput():
    global goal, graph, heuristics, isAscending

    n = int(input("Enter the number of nodes: "))

    for _ in range(n):
        name = input("\nNode: ").strip()
        val = int(input("Heuristics: "))
        children = input("Neighbors: ").strip()

        heuristics[name] = val
        graph[name] = [c.strip() for c in children.split()] if children else []

    start = input("\nEnter start node: ").strip()
    goal = input("Enter goal node: ").strip()

    if heuristics[start] < heuristics[goal]:
        isAscending = True
    else:
        isAscending = False

    return start

start = GetUserInput()
path = HillClimbing(start)

if path:
    print(f"\nPath: {' -> '.join(path)}")
else:
    print("\nNo path found.")