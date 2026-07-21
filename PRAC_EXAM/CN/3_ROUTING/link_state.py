from math import inf


def read_graph():
    vertices = int(input("Number of routers: "))
    edges = int(input("Number of links: "))

    graph = {i: [] for i in range(vertices)}
    print("Enter each link as: source destination cost")
    for _ in range(edges):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph, vertices


def show_table(distances):
    print("Router\tDistance")
    for node in sorted(distances):
        value = "INF" if distances[node] == inf else distances[node]
        print(f"{node}\t{value}")


def dijkstra(graph, start):
    distances = {node: inf for node in graph}
    distances[start] = 0
    visited = set()

    print("\nInitial Routing Table")
    print("-" * 48)
    show_table(distances)

    while len(visited) < len(graph):
        current_router = None
        current_distance = inf

        for node in graph:
            if node not in visited and distances[node] < current_distance:
                current_distance = distances[node]
                current_router = node

        if current_router is None:
            break

        visited.add(current_router)
        print(f"\nAfter Processing Router {current_router}")

        for neighbor, cost in graph[current_router]:
            new_distance = current_distance + cost
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

        print("-" * 48)
        show_table(distances)

    print("\nFinal Shortest Path Table")
    print("-" * 48)
    print("Destination Router\tShortest Distance")
    for node in sorted(distances):
        value = "INF" if distances[node] == inf else distances[node]
        print(f"{node}\t\t\t{value}")


def main():
    graph, _ = read_graph()
    start = int(input("Start router: "))
    if start not in graph:
        print("Invalid start router")
        return
    dijkstra(graph, start)


if __name__ == "__main__":
    main()