def get_graph_input():
    graph = {}
    heuristics = {}
    n_nodes = int(input("Enter number of nodes: "))
    for _ in range(n_nodes):
        node = input("Node: ").strip()
        heuristics[node] = int(input("Heuristic: "))
        neighbors = input("Neighbors (space separated): ").strip().split()
        graph[node] = {}
        for nb in neighbors:
            cost = int(input(f"Cost from {node} to {nb}: "))
            graph[node][nb] = cost
    return graph, heuristics

def format_tuple(node, par, g, h):
    p = par if par is not None else "nil"
    return f"({node},{p},{g},{h},{g+h})"

def print_lists(open_list, closed_list, heuristics, step):
    col_w = 28
    open_tuples   = [format_tuple(n, par, g, heuristics[n]) for n, par, g in open_list]
    closed_tuples = [format_tuple(n, par, g, heuristics[n]) for n, par, g in closed_list]
    max_rows = max(len(open_tuples), len(closed_tuples), 1)
    print(f"\nStep {step}")
    print(f"{'OPEN LIST':<{col_w}}  CLOSED LIST")
    print("-" * (col_w * 2 + 2))
    for i in range(max_rows):
        left  = open_tuples[i]   if i < len(open_tuples)   else ""
        right = closed_tuples[i] if i < len(closed_tuples) else ""
        print(f"{left:<{col_w}}  {right}")
    print("-" * (col_w * 2 + 2))

def insert_open(open_list, node, par, g, heuristics):
    f_new = g + heuristics[node]
    for i, (n, p, gv) in enumerate(open_list):
        if f_new <= gv + heuristics[n]:
            open_list.insert(i, (node, par, g))
            return
    open_list.append((node, par, g))

def update_open(open_list, node, par, g, heuristics):
    for i, (n, p, gv) in enumerate(open_list):
        if n == node:
            open_list.pop(i)
            break
    insert_open(open_list, node, par, g, heuristics)

def reconstruct_path(node, parent_map):
    path = []
    while node is not None:
        path.append(node)
        node = parent_map[node]
    return list(reversed(path))

def propagate_improvement(m, graph, heuristics, open_list, closed_list, parent_map, g):
    for s in graph.get(m, {}).keys():
        new_g = g[m] + graph[m][s]
        if new_g < g.get(s, float('inf')):
            parent_map[s] = m
            g[s] = new_g
            in_open   = any(n == s for n, _, _ in open_list)
            in_closed = any(n == s for n, _, _ in closed_list)
            if in_open:
                update_open(open_list, s, parent_map[s], g[s], heuristics)
            if in_closed:
                for i, (n, p, gv) in enumerate(closed_list):
                    if n == s:
                        closed_list[i] = (s, parent_map[s], g[s])
                        break
                propagate_improvement(s, graph, heuristics, open_list, closed_list, parent_map, g)

def astar(graph, heuristics, start, goal):
    open_list   = []   
    closed_list = []   
    parent_map  = {}
    g           = {}

    g[start]          = 0
    parent_map[start] = None
    insert_open(open_list, start, None, 0, heuristics)

    step = 0

    while open_list:
        step += 1
        print_lists(open_list, closed_list, heuristics, step)
        n, n_par, n_g = open_list.pop(0)

        closed_list.insert(0, (n, n_par, n_g))

        if n == goal:
            path = reconstruct_path(n, parent_map)
            print(f"\nGOAL '{goal}' REACHED!")
            print(f"PATH : {' -> '.join(path)}")
            print(f"COST : {g[n]}")
            return path

        for m in graph.get(n, {}).keys():
            k_n_m     = graph[n][m]
            in_open   = any(nd == m for nd, _, _ in open_list)
            in_closed = any(nd == m for nd, _, _ in closed_list)

            if not in_open and not in_closed:
                parent_map[m] = n
                g[m]          = g[n] + k_n_m
                insert_open(open_list, m, parent_map[m], g[m], heuristics)

            elif in_open:
                if (g[n] + k_n_m) < g.get(m, float('inf')):
                    parent_map[m] = n
                    g[m]          = g[n] + k_n_m
                    update_open(open_list, m, parent_map[m], g[m], heuristics)

            elif in_closed:
                if (g[n] + k_n_m) < g.get(m, float('inf')):
                    parent_map[m] = n
                    g[m]          = g[n] + k_n_m
                    for i, (nd, p, gv) in enumerate(closed_list):
                        if nd == m:
                            closed_list[i] = (m, parent_map[m], g[m])
                            break
                    propagate_improvement(m, graph, heuristics, open_list, closed_list, parent_map, g)

    print("\nFAILURE: No path found.")
    return None


print("========== A* Algorithm ==========")
graph, heuristics = get_graph_input()
start = input("Start node: ").strip()
goal  = input("Goal node: ").strip()
astar(graph, heuristics, start, goal)