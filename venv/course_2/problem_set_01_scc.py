"""
Kosaraju's 2 Pass Algorithm for computing Strongly Connected Components


The file contains the edges of a directed graph. Vertices are labeled as positive integers from 1 to 875714. Every row indicates an edge, the vertex label in first column is the tail and the vertex label in second column is the head (recall the graph is directed, and the edges are directed from the first column vertex to the second column vertex). So for example, the 11^{th}11
th
  row looks liks : "2 47646". This just means that the vertex with label 2 has an outgoing edge to the vertex with label 47646

Your task is to code up the algorithm from the video lectures for computing strongly connected components (SCCs), and to run this algorithm on the given graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given graph, in decreasing order of sizes, separated by commas (avoid any spaces). So if your algorithm computes the sizes of the five largest SCCs to be 500, 400, 300, 200 and 100, then your answer should be "500,400,300,200,100" (without the quotes). If your algorithm finds less than 5 SCCs, then write 0 for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose sizes are 400, 300, and 100, then your answer should be "400,300,100,0,0" (without the quotes).  (Note also that your answer should not have any spaces in it.)

WARNING: This is the most challenging programming assignment of the course. Because of the size of the graph you may have to manage memory carefully. The best way to do this depends on your programming language and environment, and we strongly suggest that you exchange tips for doing this on the discussion forums.

1 point

"""


import constants
from constants import compose
from constants import deepcopy
from constants import pp
from stack import Stack


def list_to_int(l):
    return map(int, l)


class Node:
    def __init__(self, index=-1):
        self.index = index
        self.successors = set()
        self.predecessors = set()
        self.visited_forward = False
        self.visited_backward = False
        self.finish_time_forward = 0
        self.finish_time_backward = 0
        self.leader_forward = -1
        self.leader_backward = -1

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def get_neighbors(self, forward=True):
        return self.successors if forward else self.predecessors

    def add_neighbor(self, neighbor, forward=True):
        neighbors = self.successors if forward else self.predecessors
        neighbors.add(neighbor)

    def get_visited(self, forward=True):
        return self.visited_forward if forward else self.visited_backward

    def get_unvisited(self, forward=True):
        return not self.get_visited(forward)

    def set_visited(self, forward=True):
        if forward:
            self.visited_forward = True
        else:
            self.visited_backward = True

    def set_unvisited(self, forward=True):
        if forward:
            self.visited_forward = False
        else:
            self.visited_backward = False

    def get_finish_time(self, forward=True):
        return self.finish_time_forward if forward else self.finish_time_backward

    def set_finish_time(self, time, forward=True):
        if forward:
            self.finish_time_forward = time
        else:
            self.finish_time_backward = time

    def get_leader(self, forward=True):
        return self.leader_forward if forward else self.leader_backward

    def set_leader(self, leader, forward=True):
        if forward:
            self.leader_forward = leader
        else:
            self.leader_backward = leader

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class DiGraph:
    def __init__(self, filename):
        self.graph = dict()
        with open(filename, "r") as f:
            maps = [list_to_int, str.split, str.strip]
            edges = map(compose(*maps), filter(lambda x: not x.isspace(), f))
            for edge in edges:
                self.add_edge(edge)

    def add_arc(self, start, end, forward=True):
        tail = self.graph.get(start, Node(start))
        tail.add_neighbor(end, forward)
        self.graph[start] = tail

    def add_edge(self, edge):
        start, end = edge
        self.add_arc(start, end, forward=True)
        self.add_arc(end, start, forward=False)

    def get_neighbors(self, node, forward=True):
        indices = node.get_neighbors(forward)
        return map(self.graph.get, indices)

    def get_unvisited_all(self, node, forward=True):
        return filter(
                        lambda x: x.get_unvisited(forward),
                        self.get_neighbors(node, forward)
                     )

    # noinspection PyShadowingBuiltins
    def get_next(self, node, forward=True):
        all = self.get_unvisited_all(node, forward)
        for n in all:
            if n:
                return n
        return None


    @staticmethod
    def visit(node, forward=True):
        node.set_visited(forward)

    def dfs(self, node, leader, time, size, forward=True):
        if not node or node.get_visited(forward):
            return
        node.set_leader(leader, forward)
        DiGraph.visit(node, forward)
        neighbors = self.get_unvisited_all(node, forward)
        for neighbor in neighbors:
            self.dfs(neighbor, leader, time, size, forward)
        time[0], size[0] = time[0] + 1, size[0] + 1
        node.set_finish_time(time[0], forward)


    def dfs_stack(self, node, leader, time, size, forward=True):
        if not node:
            return
        stack = Stack()
        node.set_leader(leader, forward)
        DiGraph.visit(node, forward)
        stack.push(node)
        while node := stack.top():
            if node := self.get_next(node, forward):
                DiGraph.visit(node, forward)
                stack.push(node)
            else:
                node = stack.pop()
                if node is not None:
                    time[0], size[0] = time[0] + 1, size[0] + 1
                    node.set_finish_time(time[0], forward)

    def traversal(self, indices=None, forward=True):
        time, sizes = [0], []
        indices = self.graph.keys() if not indices else indices
        for index in indices:
            size = [0]
            node = self.graph[index]
            if not node.get_visited(forward):
                self.dfs_stack(node, index, time, size, forward)
            sizes.append(size[0])
        return sizes

    def forward_traversal(self, indices=None):
        return self.traversal(indices, forward=True)

    def backward_traversal(self, indices=None):
        return self.traversal(indices, forward=False)

    def compute_scc(self, num=5):
        self.backward_traversal()
        nodes = sorted(self.graph.items(), reverse=True, key=lambda x: x[1].get_finish_time(forward=False))
        indices = list(map(lambda x: x[1].get_index(), nodes))
        sizes = sorted(self.forward_traversal(indices), reverse=True)
        return sizes[:num]


def test():
    assert DiGraph('test_case_01.txt').compute_scc() == [3, 3, 3, 0, 0]
    assert DiGraph('test_case_02.txt').compute_scc() == [3, 3, 2, 0, 0]
    assert DiGraph('test_case_03.txt').compute_scc() == [3, 3, 1, 1, 0]
    assert DiGraph('test_case_04.txt').compute_scc() == [7, 1, 0, 0, 0]
    assert DiGraph('test_case_05.txt').compute_scc() == [6, 3, 2, 1, 0]
    assert DiGraph('test_case_06.txt').compute_scc() == [3, 1, 1, 0, 0]


if __name__ == constants.MAIN:
    from time import time

    start = time()
    sizes = DiGraph('problem_set_01_scc.txt').compute_scc()
    end = time()
    print(f'sizes = {sizes}')
    print(f'time = {end - start}')

    # sizes = [434821, 968, 459, 313, 211]
    # time = 146.5 seconds with get_next implemented using list
    # time = 69.6 seonds with get_next implemented using filter

