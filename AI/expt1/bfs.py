from collections import deque

def bfs(graph, start):
    visited = []
    queue = deque()

    print("BFS Traversal: ")

    visited.append(start)
    queue.append(start)

    while queue:
        vertex = queue.popleft()
        print(vertex, end=' ')

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

graph = {}

n = int(input("Enter the number of vertices: "))

for i in range(n):
    v = input(f"\nEnter vertex {i + 1}: ")
    neighbors = input(f"Enter the neighbors of {v}: ").split()
    graph[v] = neighbors

start = input("\nEnter the starting vertex: ")

bfs(graph, start)