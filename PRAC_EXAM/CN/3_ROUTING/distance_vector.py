from math import inf


def read_edges():
    vertices = int(input("Number of routers: "))
    edges = int(input("Number of directed links: "))

    edge_list = []
    print("Enter each link as: source destination cost")
    for _ in range(edges):
        u, v, w = map(int, input().split())
        edge_list.append((u, v, w))
    return edge_list, vertices


def show_table(distance):
    for node in range(len(distance)):
        value = "INF" if distance[node] == inf else distance[node]
        print(f"Router {node} --> {value}")


def bellman_ford(edges, vertices, source):
    distance = [inf] * vertices
    distance[source] = 0

    print("\nInitial Routing Table")
    print("-" * 48)
    show_table(distance)

    for iteration in range(vertices - 1):
        print(f"\nIteration {iteration + 1}")
        print("-" * 48)

        updated = False
        for u, v, w in edges:
            if distance[u] != inf and distance[u] + w < distance[v]:
                old_distance = distance[v]
                distance[v] = distance[u] + w
                updated = True

                print(f"Updating Router {v}")
                print(f"Path: Router {u} -> Router {v}")
                print(f"Edge Cost = {w}")
                print(f"Old Distance = {old_distance if old_distance != inf else 'INF'}")
                print(f"New Distance = {distance[v]}")
                print()

        print("Routing Table After Iteration")
        print("-" * 48)
        show_table(distance)

        if not updated:
            print("\nNo further updates possible.")
            break

    print("\nFinal Routing Table")
    print("-" * 48)
    print("Destination Router\tMinimum Distance")
    for node in range(vertices):
        value = "INF" if distance[node] == inf else distance[node]
        print(f"{node}\t\t\t{value}")


def main():
    edges, vertices = read_edges()
    source = int(input("Source router: "))
    if source < 0 or source >= vertices:
        print("Invalid source router")
        return
    bellman_ford(edges, vertices, source)


if __name__ == "__main__":
    main()