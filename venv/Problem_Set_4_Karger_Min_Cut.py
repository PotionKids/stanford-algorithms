import random


class Graph:
    def __init__(self, filename):
        self.graph = create_graph_from(filename)
        self.vertices = list(self.graph.keys())

    @staticmethod
    def add_neighbors(vertex_a, vertex_b):
        result = vertex_a
        for neighbor, num_edges in vertex_b.items():
            if neighbor in result:
                result[neighbor] += num_edges
            result[neighbor] = num_edges
        return result

    def collapse_edge(self, vertex_a, vertex_b):
        neighbors_of_b = self.graph[vertex_b]
        for neighbor in neighbors_of_b:
            if neighbor != vertex_a:
                self.graph[neighbor][vertex_a] = \
                    self.graph[neighbor].get(vertex_a, 0) +\
                    self.graph[neighbor][vertex_b]
                self.graph[neighbor].pop(vertex_b)

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
    head = random.choice(graph.vertices)
    tail = random.choice(list(graph.graph[head].keys()))
    print(f"head = {head}, tail = {tail}")
    try:
        assert head in graph.vertices
        assert tail in graph.vertices
    except AssertionError:
        print('assertion error')
        print(f"missing head = {head}, tail = {tail}")
        pprint.pp(graph.graph)
    return head, tail


# noinspection PyShadowingNames
def karger_min_cut(graph):
    if len(graph.vertices) < 3:
        return graph

    while len(graph.vertices) > 2:
        head, tail = select_edge(graph)
        graph.collapse_edge(head, tail)

    return graph


if __name__ == '__main__':
    import pprint

    graph = Graph('Problem_Set_4_Karger_Min_Cut.txt')
    # graph = Graph('Problem_Set_4_Karger_Min_Cut_dummy.txt')

    pprint.pp(graph.graph)
    reduced = karger_min_cut(graph)
    pprint.pp(reduced.graph)
    print(reduced.vertices)