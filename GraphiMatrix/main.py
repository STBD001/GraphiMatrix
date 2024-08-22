import random
import time
import heapq

class InvalidArgumentException(Exception):
    def __str__(self):
        return "Invalid argument"

class LogicErrorException(Exception):
    def __str__(self):
        return "Logic error"

class Graph:
    def __init__(self, num_vertices):
        self.adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.vertices_data = [0] * num_vertices

    def end_vertices(self, e):
        return [i for i in range(len(self.adjacency_matrix)) if self.adjacency_matrix[e][i] != 0]

    def opposite(self, v, e):
        if e < 0 or e >= len(self.adjacency_matrix) or v < 0 or v >= len(self.adjacency_matrix):
            raise InvalidArgumentException()
        if self.adjacency_matrix[v][e] == 0:
            raise LogicErrorException()
        for i in range(len(self.adjacency_matrix)):
            if self.adjacency_matrix[i][e] != 0 and i != v:
                return i
        raise LogicErrorException()

    def are_adjacent(self, v, w):
        return self.adjacency_matrix[v][w] != 0

    def replace(self, v, x):
        self.vertices_data[v] = x

    def replace_edge(self, e, x):
        if e < 0 or e >= len(self.adjacency_matrix):
            raise InvalidArgumentException()
        for i in range(len(self.adjacency_matrix)):
            if self.adjacency_matrix[e][i] != 0:
                self.adjacency_matrix[e][i] = x
                self.adjacency_matrix[i][e] = x

    def insert_vertex(self, o):
        self.adjacency_matrix.append([0] * len(self.adjacency_matrix))
        for row in self.adjacency_matrix:
            row.append(0)
        self.vertices_data.append(o)

    def insert_edge(self, v, w, o):
        if v < 0 or v >= len(self.adjacency_matrix) or w < 0 or w >= len(self.adjacency_matrix):
            raise InvalidArgumentException()
        self.adjacency_matrix[v][w] = o
        self.adjacency_matrix[w][v] = o

    def remove_vertex(self, v):
        if v < 0 or v >= len(self.adjacency_matrix):
            raise InvalidArgumentException()
        self.adjacency_matrix.pop(v)
        for row in self.adjacency_matrix:
            row.pop(v)
        self.vertices_data.pop(v)

    def remove_edge(self, v, w):
        if v < 0 or v >= len(self.adjacency_matrix) or w < 0 or w >= len(self.adjacency_matrix):
            raise InvalidArgumentException()
        if self.adjacency_matrix[v][w] == 0:
            raise InvalidArgumentException()
        self.adjacency_matrix[v][w] = 0
        self.adjacency_matrix[w][v] = 0

    def incident_edges(self, v):
        return [i for i in range(len(self.adjacency_matrix)) if self.adjacency_matrix[v][i] != 0]

    def get_vertices(self):
        return list(range(len(self.vertices_data)))

    def get_edges(self):
        edges = []
        for i in range(len(self.adjacency_matrix)):
            for j in range(i + 1, len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] != 0:
                    edges.append((i, j))
        return edges

    def initialize_single_source(self, source):
        self.distances = [{'distance': float('inf'), 'predecessor': -1} for _ in range(len(self.adjacency_matrix))]
        self.distances[source]['distance'] = 0

    def dijkstra(self, source):
        self.initialize_single_source(source)
        visited = [False] * len(self.adjacency_matrix)
        pq = [(0, source)]
        while pq:
            current_distance, u = heapq.heappop(pq)
            if visited[u]:
                continue
            visited[u] = True
            for v in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[u][v] != 0:
                    weight = self.adjacency_matrix[u][v]
                    if not visited[v] and self.distances[u]['distance'] + weight < self.distances[v]['distance']:
                        self.distances[v]['distance'] = self.distances[u]['distance'] + weight
                        self.distances[v]['predecessor'] = u
                        heapq.heappush(pq, (self.distances[v]['distance'], v))

    def get_path(self, source, destination):
        path = []
        v = destination
        while v != -1:
            path.append(v)
            v = self.distances[v]['predecessor']
        return path[::-1]

    def shortest_path_from_source(self, source):
        self.dijkstra(source)
        print(f"Shortest paths from vertex {source}:")
        for i in range(len(self.adjacency_matrix)):
            if i != source:
                path = self.get_path(source, i)
                print(f"Vertex {i}: ", end="")
                if self.distances[i]['distance'] == float('inf'):
                    print("No path exists")
                else:
                    print(f"Path: {' -> '.join(map(str, path))}, Distance: {self.distances[i]['distance']}")

    def shortest_path(self, source, destination):
        self.dijkstra(source)
        print(f"Shortest path from vertex {source} to vertex {destination}: ", end="")
        path = self.get_path(source, destination)
        if self.distances[destination]['distance'] == float('inf'):
            print("No path exists")
        else:
            print(f"Path: {' -> '.join(map(str, path))}, Distance: {self.distances[destination]['distance']}")

def generate_random_instances(num_vertices, density):
    instances = []
    density = min(density, 100)
    random.seed(time.time())

    for _ in range(100):
        graph = Graph(num_vertices)
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.randint(0, 99) < density:
                    weight = random.randint(1, 10)
                    graph.insert_edge(i, j, weight)
        instances.append(graph)
    return instances

def measure_shortest_path_from_source(instances):
    for i, graph in enumerate(instances):
        start = time.time()
        source_vertex = 0
        graph.shortest_path_from_source(source_vertex)
        end = time.time()
        print(f"Time taken to find shortest path for instance {i + 1}: {(end - start) * 1000:.2f} ms")

def calculate_average_time(instances):
    total_time = 0
    for i, graph in enumerate(instances):
        start = time.time()
        source_vertex = 0
        graph.shortest_path_from_source(source_vertex)
        end = time.time()
        elapsed_time = (end - start) * 1000
        total_time += elapsed_time
        print(f"Time taken to find shortest path for instance {i + 1}: {elapsed_time:.2f} ms")
    average_time = total_time / len(instances)
    print(f"\nAverage time taken to find shortest path for all instances: {average_time:.2f} ms")

def measure_shortest_path(instances, source, destination):
    for i, graph in enumerate(instances):
        start = time.time()
        graph.shortest_path(source, destination)
        end = time.time()
        print(f"Time taken to find shortest path for instance {i + 1}: {(end - start) * 1000:.2f} ms")

def calculate_average_time_for_pairs(instances, source, destination):
    total_time = 0
    for i, graph in enumerate(instances):
        start = time.time()
        graph.shortest_path(source, destination)
        end = time.time()
        elapsed_time = (end - start) * 1000
        total_time += elapsed_time
        print(f"Time taken to find shortest path for instance {i + 1}: {elapsed_time:.2f} ms")
    average_time = total_time / len(instances)
    print(f"\nAverage time taken to find shortest path for all instances: {average_time:.2f} ms")

def main():
    num_vertices = int(input("Enter number of vertices: "))
    density = int(input("Enter density (percentage): "))

    random_instances = generate_random_instances(num_vertices, density)

    measure_shortest_path_from_source(random_instances)

    source = int(input("\nEnter source vertex for shortest path calculation: "))
    destination = int(input("Enter destination vertex for shortest path calculation: "))
    measure_shortest_path(random_instances, source, destination)

    calculate_average_time_for_pairs(random_instances, source, destination)

if __name__ == "__main__":
    main()
