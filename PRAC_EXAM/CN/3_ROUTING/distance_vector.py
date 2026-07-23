from math import inf

vertices = int(input("Number of routers: "))
edges = int(input("Number of links: "))

graph = []

for _ in range(edges):
    u, v, w = map(int, input("u v w : ").split())
    graph.append((u, v, w))

source = int(input("Source router: "))


def bellman_ford():
    dist = [inf] * vertices
    dist[source] = 0

    for i in range(vertices - 1):

        for u, v, w in graph:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

        print(f"\nAfter Iteration {i + 1}")
        for j in range(vertices):
            if dist[j] == inf:
                print(j, "INF")
            else:
                print(j, dist[j])

    print("\nFinal Routing Table")
    for i in range(vertices):
        if dist[i] == inf:
            print(i, "INF")
        else:
            print(i, dist[i])


bellman_ford()