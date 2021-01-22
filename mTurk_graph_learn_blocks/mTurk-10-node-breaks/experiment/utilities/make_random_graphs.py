from utilities import graphs
import networkx as nx

g_set = graphs.generate_random_graphs(1500)
g_set = graphs.representative_graphs(g_set)

for i, g in enumerate(g_set):
    nx.write_gpickle(g, "randomgraphs/%d.gpickle"%i)