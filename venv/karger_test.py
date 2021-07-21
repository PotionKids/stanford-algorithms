import networkx as nx
import itertools
import matplotlib.pyplot as plt

G = nx.Graph()

with open('Problem_Set_4_Karger_Min_Cut.txt') as f:
    graph_dict = {}
    for line in f.readlines():
        split = line.split('\t')
        graph_dict[int(split[0])] = [int(i) for i in split[1:-1]]
        #The dict keys are nodes.
        #The dict values are the list of edge targets from this node.

G.add_nodes_from(graph_dict.keys())

for k, v in graph_dict.items():
    for edge in itertools.product([k], v):
        G.add_edge(*edge)

nx.draw(G)
plt.show()