goal = ""
graph = {}
heuristics = {}


def h(node):
    return heuristics.get(node, 99)

def find_node(lst, node):
    for item in lst:
        if item[0] == node:
            return item
    return None


def replace_node(lst, node, new_node):
    for i in range(len(lst)):
        if lst[i][0] == node:
            lst[i] = new_node
            break
    return lst

def reconstruct(curr, closed):
    path = [curr[0]]
    parent = curr[1]

    while parent is not None:
        path.insert(0, parent)
        node = find_node(closed, parent)
        parent = node[1] if node else None

    return path

def propagate_improvement(nodepair, open_list, closed):
    node, _, g, _, _ = nodepair
    for child, cost in graph.get(node, []):
        open_child = find_node(open_list, child)
        closed_child = find_node(closed, child)
        child_node = open_child if open_child else closed_child
        # Update only descendants of the current node
        if child_node and child_node[1] == node:
            new_g = g + cost
            if new_g < child_node[2]:
                new_node = (
                    child,
                    node,
                    new_g,
                    h(child),
                    new_g + h(child)
                )
                if open_child:
                    open_list = replace_node(
                        open_list,
                        child,
                        new_node
                    )
                else:
                    closed = replace_node(
                        closed,
                        child,
                        new_node
                    )
                    open_list, closed = propagate_improvement(
                        new_node,
                        open_list,
                        closed
                    )

    return open_list, closed

def astar(start):
    open_list = [(start, None, 0, h(start), h(start))]
    closed = []
    while open_list:
        # Sort according to f value
        open_list.sort(key=lambda x: x[4])
        curr = open_list.pop(0)
        node = curr[0]
        if node == goal:
            return reconstruct(curr, closed)
        closed.append(curr)
        for child, cost in graph.get(node, []):
            new_g = curr[2] + cost
            new_node = (
                child,
                node,
                new_g,
                h(child),
                new_g + h(child)
            )
            open_child = find_node(open_list, child)
            closed_child = find_node(closed, child)
            # New node
            if not open_child and not closed_child:
                open_list.append(new_node)
            # Better path found in OPEN
            elif open_child:
                if new_g < open_child[2]:
                    open_list = replace_node(
                        open_list,
                        child,
                        new_node
                    )
            # Better path found in CLOSED
            else:
                if new_g < closed_child[2]:
                    closed = replace_node(
                        closed,
                        child,
                        new_node
                    )

                    open_list, closed = propagate_improvement(
                        new_node,
                        open_list,
                        closed
                    )

    return None


def input_graph():
    global goal

    n = int(input("Enter number of nodes: "))

    for _ in range(n):

        node = input("\nNode: ").strip()
        heuristics[node] = int(input("h(Node): "))

        children = input("Neighbours: ").split()

        graph[node] = []

        for child in children:
            cost = int(input(f"Cost({node} -> {child}): "))
            graph[node].append((child, cost))

    start = input("\nEnter start node: ").strip()
    goal = input("Enter goal node: ").strip()

    return start


# Driver Code
start = input_graph()
path = astar(start)

if path:
    print("\nPath:", " -> ".join(path))
else:
    print("\nNo path found.")