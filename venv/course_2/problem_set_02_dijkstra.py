"""
Dijkstra's Shortest Path Algorithm


In this programming problem you'll code up Dijkstra's shortest-path algorithm.

Download the following text file:

dijkstraData.txt
The file contains an adjacency list representation of an undirected weighted graph with 200 vertices labeled 1 to 200.  Each row consists of the node tuples that are adjacent to that particular vertex along with the length of that edge. For example, the 6th row has 6 as the first entry indicating that this row corresponds to the vertex labeled 6. The next entry of this row "141,8200" indicates that there is an edge between vertex 6 and vertex 141 that has length 8200.  The rest of the pairs of this row indicate the other vertices adjacent to vertex 6 and the lengths of the corresponding edges.

Your task is to run Dijkstra's shortest-path algorithm on this graph, using 1 (the first vertex) as the source vertex, and to compute the shortest-path distances between 1 and every other vertex of the graph. If there is no path between a vertex vv and vertex 1, we'll define the shortest-path distance between 1 and vv to be 1000000.

You should report the shortest-path distances to the following ten vertices, in order: 7,37,59,82,99,115,133,165,188,197.  You should encode the distances as a comma-separated string of integers. So if you find that all ten of these vertices except 115 are at distance 1000 away from vertex 1 and 115 is 2000 distance away, then your answer should be 1000,1000,1000,1000,1000,2000,1000,1000,1000,1000. Remember the order of reporting DOES MATTER, and the string should be in the same order in which the above ten vertices are given. The string should not contain any spaces.  Please type your answer in the space provided.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn)O(mn) time implementation of Dijkstra's algorithm should work fine.  OPTIONAL: For those of you seeking an additional challenge, try implementing the heap-based version.  Note this requires a heap that supports deletions, and you'll probably need to maintain some kind of mapping between vertices and their positions in the heap.

1 point
"""

from heap import Heap
from heap import Pair
from constants import reduce
from constants import compose
from constants import pp
import constants


class Graph:
    MAX_DISTANCE = 1_000_000

    def __init__(self, filename):
        self.graph = {}
        with open(filename, "r") as f:
            maps = [Graph.ver_to_adj, str.split, str.strip]
            ver_edg_dicts = map(compose(*maps), f)
            for ver_edges in ver_edg_dicts:
                self.graph.update(ver_edges)

    @staticmethod
    def gen_vertices_in_graph(g):
        for vertex in g.graph.keys():
            yield vertex

    def gen_vertices(self):
        return Graph.gen_vertices_in_graph(self)

    def gen_neighbors(self, v):
        for vertex in self.graph[v]:
            yield vertex

    def neighbors(self, v):
        return {vertex for vertex in self.gen_neighbors(v)}

    def distance(self, s, v):
        return self.graph.get(s).get(v, self.MAX_DISTANCE)


    @staticmethod
    def edge_to_wt(l, sep=','):
        return {
                int(edge): int(weight)
                for edge, weight in
                map(lambda x: x.split(sep=sep), l)
               }

    @staticmethod
    def ver_to_adj(l, sep=','):
        vertex, *adj_list = l
        return {int(vertex): Graph.edge_to_wt(adj_list, sep=sep)}


class Dijkstra:
    """

    """
    def __init__(self, g, s=None):
        self.graph = g
        self.start = s
        self.map = {s: 0} if s else {}

    def set_start(self, s):
        self.start = s
        self.map = {s: 0}

    def heapify(self, s):
        return Heap(
                     pairs=Pair.pairs
                     (
                         (v, g.MAX_DISTANCE) if v != s else (v, 0)
                         for v in self.graph.gen_vertices()
                     ),
                     min=True
                   )

    def crossing_vertices(self, cut):
        return reduce(
                        set.union,
                        map(
                              self.graph.neighbors, cut
                           ),
                        set()
                     ).difference(cut)

    def neighbors(self, cut, v):
        return self.graph.neighbors(v).intersection(cut)

    def value(self, s):
        return self.map[s]

    def distance(self, s, v):
        return self.graph.distance(s, v)

    def dijk_distance(self, s, v):
        return self.map[s] + self.distance(s, v)

    def nearest(self, cut, v):
        return min(
                    self.neighbors(cut, v),
                    key=lambda s: self.dijk_distance(s, v)
                  )

    def cut_distance(self, cut, v):
        return self.dijk_distance(self.nearest(cut, v), v)

    def next(self, cut):
        return min(
                    self.crossing_vertices(cut),
                    key=lambda v: self.cut_distance(cut, v),
                    default=None
                  )

    # noinspection PyShadowingBuiltins
    def calculate(self):
        if self.start is None:
            print('Start vertex is unset. Please set it.')
            return
        cut = {self.start}
        next = self.next(cut)
        while next:
            self.map[next] = self.cut_distance(cut, next)
            cut.add(next)
            next = self.next(cut)


if __name__ == constants.MAIN:
    from time import time

    g = Graph('problem_set_02_dijkstra.txt')
    l = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    start = time()
    dijkstra = Dijkstra(g)
    dijkstra.set_start(1)
    dijkstra.calculate()
    end = time()
    print(f'time = {end - start}')
    p = [dijkstra.map[x] for x in l]
    print(*p, sep=',')


