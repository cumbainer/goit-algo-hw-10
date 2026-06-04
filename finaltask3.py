import heapq


def dijkstra(graph, start):
    distances = {vertex: float("inf") for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous


def build_path(previous, target):
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = previous[current]

    return list(reversed(path))


graph = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2, "F": 6},
    "E": {"C": 10, "D": 2, "F": 3},
    "F": {"D": 6, "E": 3},
}

start_vertex = "A"
distances, previous = dijkstra(graph, start_vertex)

print(f"Shortest paths from {start_vertex}:")
for vertex in sorted(graph):
    path = build_path(previous, vertex)
    print(f"{vertex}: distance={distances[vertex]}, path={' -> '.join(path)}")
