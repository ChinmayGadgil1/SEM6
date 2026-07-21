goal = ""
graph = {}
heuristics = {}

def h(node):
    return heuristics.get(node, 99)

def hill_climbing(start):
    node = start
    path = [node]
    visited = {node}
    
    print("\nHill Climbing\nIter | Current | Better Neighbor")
    iteration = 1
    
    while True:
        neighbors = [n for n in graph.get(node, []) if n not in visited]
        
        if not neighbors:
            print(f"{iteration:<4} | {node:<7} | None (stuck at local optimum)")
            return path
        
        better = None
        for n in neighbors:
            if h(n) < h(node):
                better = n
                break
        
        print(f"{iteration:<4} | {node:<7} | {better if better else 'None'}")
        
        if not better:
            return path
        
        node = better
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
        h_val = int(input(f"Heuristic: "))
        neighbors = input("Neighbors: ").strip()
        
        heuristics[name] = h_val
        graph[name] = [x.strip() for x in neighbors.split() if x.strip()]
    
    start = input("Start: ").strip()
    goal = input("Goal: ").strip()
    
    return start

start = input_graph()
path = hill_climbing(start)
print(f"\nPath: {' -> '.join(path)}")
