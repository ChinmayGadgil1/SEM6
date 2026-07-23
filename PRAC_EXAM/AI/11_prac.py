def h(node):
    return heuristic.get(node, 999)


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


def propagate_improvement(curr, open_list, closed_list):
    node = curr[0]
    g = curr[3]

    for child, cost in graph[node]:

        open_child = find_node(open_list, child)
        closed_child = find_node(closed_list, child)

        child_node = open_child if open_child else closed_child

        # Check whether child is actually a descendant of node
        if child_node and child_node[1] == node:

            new_g = g + cost

            if new_g < child_node[3]:

                new_tuple = (
                    child,
                    node,
                    h(child),
                    new_g,
                    new_g + h(child)
                )

                if open_child:
                    open_list = replace_node(
                        open_list,
                        child,
                        new_tuple
                    )

                else:
                    closed_list = replace_node(
                        closed_list,
                        child,
                        new_tuple
                    )

                    open_list, closed_list = propagate_improvement(
                        new_tuple,
                        open_list,
                        closed_list
                    )

    return open_list, closed_list


def bestfs(start, goal, graph):

    open_list = [(start, None, h(start), 0, h(start))]
    closed_list = []

    parent = {}
    parent[start] = None

    while open_list:

        curr = open_list[0]
        node = curr[0]

        if node == goal:

            path = []
            p = node

            while p is not None:
                path.append(p)
                p = parent[p]

            print("\nPath:")
            print(*path[::-1], sep=" -> ")
            return

        open_list = open_list[1:]
        closed_list.insert(0, curr)

        for new_node, cost in graph[node]:

            g = cost + curr[3]
            f = g + h(new_node)

            new_tuple = (
                new_node,
                node,
                h(new_node),
                g,
                f
            )

            open_child = find_node(open_list, new_node)
            closed_child = find_node(closed_list, new_node)

            # New node
            if not open_child and not closed_child:

                open_list.append(new_tuple)
                parent[new_node] = node

            # Better path found in OPEN
            elif open_child:

                if g < open_child[3]:

                    open_list = replace_node(
                        open_list,
                        new_node,
                        new_tuple
                    )

                    parent[new_node] = node

            # Better path found in CLOSED
            else:

                if g < closed_child[3]:

                    closed_list = replace_node(
                        closed_list,
                        new_node,
                        new_tuple
                    )

                    parent[new_node] = node

                    open_list, closed_list = propagate_improvement(
                        new_tuple,
                        open_list,
                        closed_list
                    )

        open_list.sort(key=lambda x: x[4])

    print("\nNo path found.")


graph = {}
heuristic = {}

n = int(input("Enter the number of nodes: "))

for _ in range(n):

    name = input("\nNode: ").strip()
    val = int(input("Heuristic: "))
    children = input("Neighbors (space-separated): ").split()

    heuristic[name] = val
    graph[name] = []

    for ch in children:
        cost = int(input(f"Enter cost from {name} to {ch}: "))
        graph[name].append((ch, cost))


start = input("\nEnter start node: ").strip()
goal = input("Enter goal node: ").strip()

bestfs(start, goal, graph)