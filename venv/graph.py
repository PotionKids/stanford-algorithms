class Vertex:
    def __init__(self, value=None):
        self.value = value
        self.neighbors = list()
        self.visited = False

    def visit(self):
        self.visited = True

    def has_been_visited(self):
        return self.visited

    def get_neighbors(self):
        return self.neighbors

    def __str__(self):
        return f"value = {self.value}"

    def __repr__(self):
        return f"value = {self.value}, visited = {self.visited}, neighbors = {self.neighbors}"


class Graph:
    def __init__(self, filename):
        with open(filename, "r") as f:
            print(f"opened file {filename}")
            self.graph = dict()
            adj_list = [list(map(lambda x: int(x), l.strip().split())) for l in f.readlines()]
            print(adj_list)
            for indices in adj_list:
                self.graph[indices[0]] = Vertex(indices[0])
            for indices in adj_list:
                for index in indices[1:]:
                    self.graph[indices[0]].neighbors.append(index)
            self.vertices = list(self.graph.keys())
