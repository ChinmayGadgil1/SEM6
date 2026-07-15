import heapq
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
    for node in sorted(distances):
        value = "INF" if distances[node] == inf else distances[node]
        print(f"Router {node} --> {value}")


def dijkstra(graph, start):
    distances = {node: inf for node in graph}
    distances[start] = 0
    visited = set()
    heap = [(0, start)]

    print("\nInitial Routing Table")
    print("-" * 48)
    show_table(distances)

    while heap:
        current_distance, current_router = heapq.heappop(heap)
        if current_router in visited:
            continue

        visited.add(current_router)
        print(f"\nProcessing Router {current_router}")
        print("-" * 48)

        for neighbor, cost in graph[current_router]:
            print(f"Checking Path: {current_router} -> {neighbor}")
            print(f"Link Cost = {cost}")

            new_distance = current_distance + cost
            if new_distance < distances[neighbor]:
                old_distance = distances[neighbor]
                distances[neighbor] = new_distance
                print(f"Updating Router {neighbor}")
                print(f"Old Distance = {old_distance if old_distance != inf else 'INF'}")
                print(f"New Distance = {new_distance}")
                heapq.heappush(heap, (new_distance, neighbor))
            else:
                print("No Update Required")
            print()

        print("Routing Table After Processing")
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