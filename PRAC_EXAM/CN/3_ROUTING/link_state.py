INF = 999999

vertices = int(input("Number of routers: "))
edges = int(input("Number of links: "))

graph = [[] for _ in range(vertices)]

for _ in range(edges):
    u, v, w = map(int, input("u v w : ").split())
    graph[u].append((v, w))
    graph[v].append((u, w))      # Remove this line if links are directed

source = int(input("Start router: "))

dist = [INF] * vertices
visited = [False] * vertices

dist[source] = 0

for _ in range(vertices):

    # Find the unvisited router having minimum distance
    current = -1
    minimum = INF

    for i in range(vertices):
        if not visited[i] and dist[i] < minimum:
            minimum = dist[i]
            current = i

    if current == -1:
        break

    visited[current] = True

    # Update distances of neighbours
    for neighbour, cost in graph[current]:
        if dist[current] + cost < dist[neighbour]:
            dist[neighbour] = dist[current] + cost

    print("\nAfter processing router", current)
    for i in range(vertices):
        if dist[i] == INF:
            print(i, "INF")
        else:
            print(i, dist[i])

print("\nFinal Routing Table")
for i in range(vertices):
    if dist[i] == INF:
        print(i, "INF")
    else:
        print(i, dist[i])