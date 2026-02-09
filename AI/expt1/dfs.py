from collections import deque

def dfs(graph, start):
    visited = []
    stack = deque()

    print("BFS Traversal: ", end="")

    stack.append(start)

    while stack:
        vertex = stack.pop()

        if vertex not in visited:
            visited.append(vertex)
            print(vertex, end=" ")

            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)


graph = {}

n = int(input("Enter the number of vertices: "))

for i in range(n):
    v = input(f"\nEnter vertex {i + 1}: ")
    neighbors = input(f"Enter the neighbors of {v}: ").split()
    graph[v] = neighbors

start = input("\nEnter the starting vertex: ")

dfs(graph, start)