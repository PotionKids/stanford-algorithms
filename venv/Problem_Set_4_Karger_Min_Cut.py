from random import choice as pick


class Graph:
    def __init__(self, filename):
        self.graph = create_graph_from(filename)
        self.vertices = list(self.graph.keys())

    def num_vertices(self):
        return len(self.vertices)

    def adj(self, a):
        return self.graph[a]

    def adj_list(self, a):
        return list(self.adj(a).keys())

    def adjs(self, a, b):
        return self.adj(a), self.adj(b)

    def order(self, a):
        adj_a = self.adj(a)
        return sum(adj_a[b] for b in adj_a)

    def min_order(self):
        return min(self.order(a) for a in self.vertices)

    def max_order(self):
        return max(self.order(a) for a in self.vertices)

    def num_edges(self):
        return sum(self.order(a) for a in self.vertices) // 2

    def min_order_vertices(self):
        min = self.min_order()
        return list(filter(lambda x: self.order(x) == min, self.vertices))

    def max_order_vertices(self):
        max = self.max_order()
        return list(filter(lambda a: self.order(a) == max, self.vertices))

    def clean(self, a, b):
        adj_a, adj_b = self.adjs(a, b)
        adj_b.pop(b, None)
        adj_b.pop(a, None)
        adj_a.pop(b, None)
        adj_a.pop(a, None)

    def remove(self, a):
        self.graph.pop(a, None)
        self.vertices.remove(a)

    def cut(self):
        head, tail = tuple(self.graph.keys())
        return self.graph[head][tail]

    def append_neighbors(self, a, b):
        adj_a, adj_b = self.adjs(a, b)

        for n in adj_b:
            if n != a:
                adj_n = self.adj(n)
                adj_n[a] = adj_n.get(a, 0) + adj_n[b]
                adj_a[n] = adj_n[a]
                adj_n.pop(b, None)

    def contract(self, a, b):
        self.append_neighbors(a, b)
        self.clean(a, b)
        self.remove(b)


# noinspection PyShadowingNames
def create_graph_from(filename):
    with open(filename, "r") as f:
        adj_list = [list(map(lambda x: int(x), l.strip().split())) for l in f.readlines()]

    graph = dict()
    for vertices in adj_list:
        vertex, neighbors = vertices[0], vertices[1:]
        neighbors_dict = {v: neighbors.count(v) for v in neighbors}
        graph[vertex] = neighbors_dict
    return graph


# noinspection PyShadowingNames
def select_edge(g):
    head = pick(g.vertices)
    tail = pick(g.adj_list(head))
    return head, tail


# noinspection PyShadowingNames
def karger_cut(g):
    while g.num_vertices() > 2:
        a, b = select_edge(g)
        g.contract(a, b)
    return g


# noinspection PyShadowingNames
def karger_min_cut(g, max_it=1000000):
    from copy import deepcopy as dc

    min, it = g.max_order(), 0
    while it < max_it:
        cut = karger_cut(dc(g)).cut()
        min = cut if cut < min else min
        it += 1
    return min


if __name__ == '__main__':
    g = Graph('Problem_Set_4_Karger_Min_Cut.txt')
    min_cut, contracted = karger_min_cut(g, g.num_vertices()**2)