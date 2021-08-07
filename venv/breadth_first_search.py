from graph import *
from queue import Queue
import os
os.chdir('../')


def breadth_first_search(graph, index, visit=lambda v: v.visit()):
    q = Queue([index])
    while q.is_not_empty():
        ind = q.deq()
        vertex = graph.graph[v]
        visit(vertex)
        q.enq(vertex.neighbors)


if __name__ == '__main__':
    cwd = os.getcwd()
    print(f"cwd = {cwd}")
    from pprint import pp
    # graph = Graph('problem_set_1_scc.txt')
    # pp(graph.graph)

