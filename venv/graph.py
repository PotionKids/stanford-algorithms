class Vertex:
    def __init__(self, value=None):
        self.value = value
        self.neighbors = list()
        self.visited = False

    def has_been_visited(self):
        return self.visited

    def get_neighbors(self):
        return self.neighbors


class Graph:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.graph = dict()
            adj_list = [list(map(lambda x: int(x), l.strip().split())) for l in f.readlines()]
            for indices in adj_list:
                self.graph[indices[0]] = Vertex(indices[0])
            for indices in adj_list:
                for index in indices[1:]:
                    self.graph[indices[0]].neighbors.append(self.graph[index])
            self.vertices = list(self.graph.keys())
