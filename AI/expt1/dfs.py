def dfs(graph, start, visited=None):
    if visited is None:
        visited = []
    
    visited.append(start)
    print(start, end=" ")
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    
    return visited


graph = {}

n = int(input("Enter the number of vertices: "))

for i in range(n):
    v = input(f"\nEnter vertex {i + 1}: ")
    neighbors = input(f"Enter the neighbors of {v}: ").split()
    graph[v] = neighbors

start = input("\nEnter the starting vertex: ")

print("DFS Traversal: ", end="")
dfs(graph, start)
