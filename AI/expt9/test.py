goal = ""
graph = {}
heuristics = {}
Nil = None


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


def FindNode(list, node):
    return next((item for item in list if item[0] == node), Nil)


def RemoveNode(list, node):
    return [item for item in list if item[0] != node]


def ReplaceNode(list, node, new_node):
    return [new_node if item[0] == node else item for item in list]


def Sort_f(list):
    return sorted(list, key=lambda x: (x[4], x[3], x[0]))


def ReconstructPath(nodepair, closed):
    path = [nodepair[0]]
    parent = nodepair[1]

    while parent is not Nil:
        path.append(parent)
        node = next((item for item in closed if item[0] == parent), Nil)
        parent = node[1] if node else Nil

    path.reverse()
    return path


def PropagateImprovement(nodepair, open, closed):
    neighbours = MoveGen(nodepair[0])

    for child, cost in neighbours:
        open_child = FindNode(open, child)
        closed_child = FindNode(closed, child)
        child_node = open_child if open_child is not Nil else closed_child

        if child_node is not Nil and child_node[1] == nodepair[0]:
            new_g = nodepair[2] + cost

            if new_g < child_node[2]:
                new_h = h(child)
                updated_child = (child, nodepair[0], new_g, new_h, new_g + new_h)

                if open_child is not Nil:
                    open = ReplaceNode(open, child, updated_child)
                else:
                    closed = ReplaceNode(closed, child, updated_child)
                    open, closed = PropagateImprovement(updated_child, open, closed)

    return open, closed


def AStarSearch(start):
    start_h = h(start)
    open = [(start, Nil, 0, start_h, start_h)]
    closed = []
    iteration = 1

    while open:
        open = Sort_f(open)
        nodepair = Head(open)
        node = nodepair[0]

        print(f"\nIteration {iteration}:")
        print("OPEN  :", str(open).replace("None", "Nil"))
        print("CLOSED:", str(closed).replace("None", "Nil"))

        if GoalTest(node):
            print(f"\nIteration {iteration + 1}:")
            print("Goal Found")
            return ReconstructPath(nodepair, closed)

        open = Tail(open)
        closed = Cons(nodepair, closed)
        neighbours = MoveGen(node)

        for child, cost in neighbours:
            new_g = nodepair[2] + cost
            new_h = h(child)
            new_f = new_g + new_h
            new_node = (child, node, new_g, new_h, new_f)

            open_child = FindNode(open, child)
            closed_child = FindNode(closed, child)

            if open_child is Nil and closed_child is Nil:
                open = Append(open, [new_node])

            elif open_child is not Nil:
                if new_g < open_child[2]:
                    open = ReplaceNode(open, child, new_node)

            else:
                if new_g < closed_child[2]:
                    closed = ReplaceNode(closed, child, new_node)
                    open, closed = PropagateImprovement(new_node, open, closed)

        iteration += 1

    return None


def GetUserInput():
    global goal, graph, heuristics
    n = int(input("Enter the number of nodes: "))

    for _ in range(n):
        name = input("\nNode: ")
        val = float(input("h(Node): "))  # Changed to float
        children = input("Neighbors: ").split()

        weighted_children = []
        for child in children:
            cost = float(input(f"cost({name}->{child}): "))  # Changed to float
            weighted_children.append((child, cost))

        heuristics[name] = val
        graph[name] = weighted_children

    start = input("\nEnter start node: ")
    goal = input("Enter goal node: ")
    return start

start = GetUserInput()
path = AStarSearch(start)

if path:
    print(f"\nPath: {' -> '.join(path)}")
else:
    print("\nNo path found.")
