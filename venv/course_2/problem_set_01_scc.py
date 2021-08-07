import constants
from constants import compose
from constants import deepcopy
from constants import pp
import sys
# sys.setrecursionlimit(5000)


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

    def set_visited(self, forward=True):
        if forward:
            self.visited_forward = True
        else:
            self.visited_backward = True

    def get_finish_time(self, forward=True):
        return self.finish_time_forward if forward else self.finish_time_backward

    def set_finish_time(self, time, forward=True):
        # print(f'set finish time = {time} for forward = {forward}')
        if forward:
            self.finish_time_forward = time
        elif not forward:
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
            count = 0
            for edge in edges:
                self.add_edge(edge)
                count += 1
                if count > 250000:
                    break

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

    @staticmethod
    def visit(node, forward=True):
        node.set_visited(forward)

    def dfs(self, node, leader, time, size, forward=True):
        # print(f'time = {time}')
        if node.get_visited(forward):
            return

        node.set_leader(leader, forward)
        DiGraph.visit(node, forward)
        neighbors = self.get_neighbors(node, forward)
        for neighbor in neighbors:
            self.dfs(neighbor, leader, time, size, forward)
        time[0] += 1
        size[0] += 1
        # print(f'time = {time}, forward = {forward}')
        node.set_finish_time(time[0], forward)


    def dfs_stack(self, node, leader, time, size, forward=True):
        from collections import deque
        return self

    def traversal(self, indices=None, forward=True):
        time = [0]
        sizes = []
        indices = self.graph.keys() if not indices else indices
        for index in indices:
            # print(f'index = {index} inside traversal')
            size = [0]
            node = self.graph[index]
            self.dfs(node, index, time, size, forward)
            sizes.append(size[0])
        # print(f'sizes inside traversal = {sizes}')
        return sizes

    def forward_traversal(self, indices=None):
        sizes = self.traversal(indices, forward=True)
        # print(f'sizes inside forward traversal = {sizes}')
        return sizes

    def backward_traversal(self, indices=None):
        sizes = self.traversal(indices, forward=False)
        # print(f'sizes inside backward traversal = {sizes}')
        return sizes

    def compute_scc(self, num=5):
        self.backward_traversal()
        nodes = sorted(self.graph.items(), reverse=True, key=lambda x: x[1].get_finish_time(forward=False))
        indices = list(map(lambda x: x[1].get_index(), nodes))
        sizes = sorted(self.forward_traversal(indices), reverse=True)
        print(f'sizes in compute_scc = {sizes[:num]}')
        return sizes[:num]


def test():
    assert DiGraph('test_case_01.txt').compute_scc() == [3, 3, 3, 0, 0]
    assert DiGraph('test_case_02.txt').compute_scc() == [3, 3, 2, 0, 0]
    assert DiGraph('test_case_03.txt').compute_scc() == [3, 3, 1, 1, 0]
    assert DiGraph('test_case_04.txt').compute_scc() == [7, 1, 0, 0, 0]
    assert DiGraph('test_case_05.txt').compute_scc() == [6, 3, 2, 1, 0]
    assert DiGraph('test_case_06.txt').compute_scc() == [3, 1, 1, 0, 0]


if __name__ == constants.MAIN:
    test()
    # dg = DiGraph('problem_set_01_scc.txt')
    # dg = DiGraph('test_case_01.txt')
    # dg = DiGraph('test_case_02.txt')
    # pp(dg.graph)
    # sizes = dg.compute_scc()
    # dg.backward_traversal()
    # dg.forward_traversal()
    # pp(dg.graph)

