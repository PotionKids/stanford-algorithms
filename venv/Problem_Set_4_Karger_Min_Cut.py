import random


class Graph:
    def __init__(self, filename):
        self.graph = create_graph_from(filename)
        self.vertices = list(self.graph.keys())

    @staticmethod
    def add_neighbors(vertex_a, vertex_b):
        result = vertex_a
        for neighbor, num_edges in vertex_b.items():
            result[neighbor] = result.get(neighbor, 0) + num_edges
        return result

    def collapse_edge(self, vertex_a, vertex_b):
        neighbors_of_b = self.graph[vertex_b]
        for neighbor in neighbors_of_b:
            if neighbor != vertex_a:
                self.graph[neighbor][vertex_a] = \
                    self.graph[neighbor].get(vertex_a, 0) +\
                    self.graph[neighbor][vertex_b]
                self.graph[neighbor].pop(vertex_b, None)

        self.graph[vertex_b].pop(vertex_b, None)
        self.graph[vertex_b].pop(vertex_a, None)
        self.graph[vertex_a] = Graph.add_neighbors(self.graph[vertex_a], self.graph[vertex_b])
        self.graph[vertex_a].pop(vertex_b, None)
        self.graph[vertex_a].pop(vertex_a, None)
        self.graph.pop(vertex_b, None)
        self.vertices.remove(vertex_b)


# noinspection PyShadowingNames
def create_graph_from(filename):
    with open(filename, "r") as file:
        adjacency_list = [list(map(lambda x: int(x), line.strip().split())) for line in file.readlines()]

    graph = dict()

    for vertices in adjacency_list:
        start = vertices[0]
        neighbors_list = vertices[1:]
        neighbors_dict = {vertex: neighbors_list.count(vertex) for vertex in neighbors_list}
        graph[start] = neighbors_dict

    return graph


# noinspection PyShadowingNames
def select_edge(graph):
    vertices = graph.vertices
    head = random.choice(graph.vertices)
    tail = random.choice(list(graph.graph[head].keys()))
    return head, tail


# noinspection PyShadowingNames
def karger_cut(graph):
    if len(graph.vertices) < 3:
        return graph

    while len(graph.vertices) > 2:
        head, tail = select_edge(graph)
        graph.collapse_edge(head, tail)

    return graph


# noinspection PyShadowingNames
def karger_min_cut(filename, max_iterations=10000000):
    min_cut = 10000
    iterations = 0
    # count = 0

    while iterations < max_iterations:
        graph = Graph(filename)
        reduced = karger_cut(graph)
        cut = 0
        head, tail = tuple(reduced.graph.keys())
        cut = reduced.graph[head][tail]
        if cut < min_cut:
            min_cut = cut
            print(f"min_cut = {min_cut}")
        iterations += 1
        if iterations % 1000 == 0:
            print(f"iteration number = {iterations}, min_cut = {min_cut}, cut = {cut}")

    print(f"min_cut = {min_cut}")
    return min_cut, reduced


if __name__ == '__main__':
    import pprint

    # graph = Graph('Problem_Set_4_Karger_Min_Cut_dummy.txt')
    graph = Graph('Problem_Set_4_Karger_Min_Cut.txt')
    min_vertices = 10000
    max_vertices = 0
    total = 0
    for vertex, neighbors in graph.graph.items():
        total += len(neighbors)
        if len(neighbors) < min_vertices:
            min_vertices = len(neighbors)
        if len(neighbors) > max_vertices:
            max_vertices = len(neighbors)

    total = total / 2
    # graph = Graph('Problem_Set_4_Karger_Min_Cut_dummy.txt')

    pprint.pp(graph.graph)
    # min_cut, reduced = karger_min_cut('Problem_Set_4_Karger_Min_Cut.txt')
    # min_cut, reduced = karger_min_cut('Problem_Set_4_Karger_Min_Cut_dummy.txt')
    # pprint.pp(reduced.graph)
    # print(f"min = {min_vertices}, max = {max_vertices}, total = {total}")