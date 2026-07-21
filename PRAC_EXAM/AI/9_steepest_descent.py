goal = ""
graph = {}
heuristics = {}

def h(node):
    return heuristics.get(node, 99)

def steepest_descent(start):
    node = start
    path = [node]
    visited = {node}
    
    print("\nSteepest Descent\nIter | Current | Best Neighbor")
    iteration = 1
    
    while True:
        neighbors = [n for n in graph.get(node, []) if n not in visited]
        
        if not neighbors:
            print(f"{iteration:<4} | {node:<7} | None (local optimum)")
            return path
        
        best_node = min(neighbors, key=lambda x: h(x))
        best_h = h(best_node)
        
        if best_h >= h(node):
            print(f"{iteration:<4} | {node:<7} | None (local optimum)")
            return path
        
        print(f"{iteration:<4} | {node:<7} | {best_node}")
        
        node = best_node
        path.append(node)
        visited.add(node)
        
        if node == goal:
            return path
        
        iteration += 1

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
path = steepest_descent(start)
print(f"\nPath: {' -> '.join(path)}")
