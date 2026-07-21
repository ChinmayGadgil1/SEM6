import heapq

goal = ""
graph = {}
heuristics = {}

def h(node):
    return heuristics.get(node, 99)

def astar(start):
    open_list = [(h(start), 0, start, None)]  # (f, g, node, parent)
    closed = {}
    
    print("\nA* Search")
    print("Iter | Node | g   | h   | f   | Status")
    iteration = 1
    
    while open_list:
        f, g, node, parent = heapq.heappop(open_list)
        
        if node in closed:
            continue
        
        closed[node] = parent
        
        print(f"{iteration:<4} | {node:<4} | {g:<3} | {h(node):<3} | {f:<3} | ", end="")
        
        if node == goal:
            path = []
            curr = node
            while curr is not None:
                path.append(curr)
                curr = closed[curr]
            path.reverse()
            print("GOAL")
            return path
        
        print("Open")
        
        for neighbor in graph.get(node, []):
            if neighbor not in closed:
                new_g = g + 1
                new_f = new_g + h(neighbor)
                heapq.heappush(open_list, (new_f, new_g, neighbor, node))
        
        iteration += 1
    
    return None

def input_graph():
    global goal, graph, heuristics
    n = int(input("Nodes: "))
    
    for _ in range(n):
        name = input("Node: ").strip()
        h_val = int(input("Heuristic: "))
        neighbors = input("Neighbors: ").strip()
        
        heuristics[name] = h_val
        graph[name] = [x.strip() for x in neighbors.split() if x.strip()]
    
    start = input("Start: ").strip()
    goal = input("Goal: ").strip()
    
    return start

start = input_graph()
path = astar(start)
if path:
    print(f"\nPath: {' -> '.join(path)}")
else:
    print("\nNo path found")
