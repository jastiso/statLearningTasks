import networkx as nx
import numpy as np
import bct
import random

random.seed()

###################
# STATIC GRAPHS
###################

_schapiro_list = {
    0: [1, 2, 3, 14],
    1: [0, 2, 3, 4],
    2: [0, 1, 3, 4],
    3: [0, 1, 2, 4],
    4: [1, 2, 3, 5],
    5: [4, 6, 7, 8],
    6: [5, 7, 8, 9],
    7: [5, 6, 8, 9],
    8: [5, 6, 7, 9],
    9: [6, 7, 8, 10],
    10: [9, 11, 12, 13],
    11: [10, 12, 13, 14],
    12: [10, 11, 13, 14],
    13: [10, 11, 12, 14],
    14: [11, 12, 13, 0]}

_lattice_list = {
    0: [1, 2, 3, 12],
    1: [0, 2, 4, 13],
    2: [0, 1, 5, 14],
    3: [0, 4, 5, 6],
    4: [1, 3, 5, 7],
    5: [2, 3, 4, 8],
    6: [3, 7, 8, 9],
    7: [4, 6, 8, 10],
    8: [5, 6, 7, 11],
    9: [6, 10, 11, 12],
    10: [7, 9, 11, 13],
    11: [8, 9, 10, 14],
    12: [0, 9, 13, 14],
    13: [1, 10, 12, 14],
    14: [2, 11, 12, 13]}

_ring_lattice_list = {
    0: [13, 14, 1, 2],
    1: [14, 0, 2, 3],
    2: [0, 1, 3, 4],
    3: [1, 2, 4, 5],
    4: [2, 3, 5, 6],
    5: [3, 4, 6, 7],
    6: [4, 5, 7, 8],
    7: [5, 6, 8, 9],
    8: [6, 7, 9, 10],
    9: [7, 8, 10, 11],
    10: [8, 9, 11, 12],
    11: [9, 10, 12, 13],
    12: [10, 11, 13, 14],
    13: [11, 12, 14, 0],
    14: [12, 13, 0, 1],
}

lattice = nx.from_dict_of_lists(_lattice_list)
schapiro = nx.from_dict_of_lists(_schapiro_list)
ring_lattice = nx.from_dict_of_lists(_ring_lattice_list)

schapiro_coords = {0: [-30, -100],
                  1: [-50, -40],
                  2: [0, -0],
                  3: [50, -40],
                  4: [30, -100],

                  5: [90, -140],
                  6: [140, -175],
                  7: [120, -240],
                  8: [70, -240],
                  9: [40, -175],

                  10: [-40, -175],
                  11: [-70, -240],
                  12: [-120, -240],
                  13: [-140, -175],
                  14: [-90, -140]}

###################
# GRAPH GENERATION
###################


def cluster_graph(nodes, clusters):
    """
    Creates a graph of <nodes> nodes, with <clusters> clusters which are
    fully interconnected except for the entry/exit nodes, which
    do not connect to each other but instead connect to neighboring
    clusters.
    """
    assert nodes % clusters == 0, 'invalid # nodes/cluster size'

    G = nx.Graph()
    for n in range(nodes):
        G.add_node(n)

    cluster_size = int(nodes / clusters)
    for c in range(clusters):
        first = c * cluster_size
        last = (c + 1) * cluster_size
        for n1 in range(first, last):
            for n2 in range(n1 + 1, last):
                G.add_edge(n1, n2)
        G.remove_edge(first, last - 1)
        G.add_edge(last - 1, last % nodes)
    return G


def cluster_transitions(nodes, clusters, sequence):
    cluster_size = int(nodes / clusters)
    cluster_id = []
    for i in range(clusters):
        cluster_id.extend([i] * cluster_size)
    
    transitions = [False]
    prev = None
    for n in sequence:
        if prev is not None:
            transitions.append(cluster_id[prev] != cluster_id[n])
        prev = n
    return transitions


def generate_random_graphs(n):
    """
    Generate n erdos-renyi graphs with 15 nodes and 30 edges,
    making sure they all have a radius of at least 3
    """
    def is_valid(G):
        if nx.number_connected_components(G) == 1:
            if nx.radius(G) >= 3:
                return True
        return False

    graphs = []
    for i in range(n):
        G = nx.gnm_random_graph(15, 30)
        while not is_valid(G):
            G = nx.gnm_random_graph(15, 30)
        graphs.append(G)
    return graphs


def graph_stats(graphs):
    """
    Given a set of graphs, compute the radius and modularity for all of them
    """
    # diameter = [nx.diameter(G) for G in graphs]
    radius = [nx.radius(G) for G in graphs]
    # ci = []
    modularity = []
    for G in graphs:
        (ci_temp, q_temp) = bct.community_louvain(np.array(nx.to_numpy_matrix(G)))
        # ci.append(ci_temp)
        modularity.append(q_temp)
    return (radius, modularity)


def representative_graphs(graphs, min_bound=0.025, max_bound=0.975):
    """
    Given a set of graphs, select the middle 95% based on modularity
    """
    n = len(graphs)
    interval_min = int(n * min_bound)
    interval_max = int(n * max_bound)
    # graphs = generate_random_graphs(n)
    (radius, modularity) = graph_stats(graphs)
    sorted_idx = np.argsort(modularity)
    middle_graphs = [graphs[i] for i in sorted_idx[interval_min:interval_max]]
    return middle_graphs


def draw_graphviz(G):
    from networkx.drawing.nx_agraph import graphviz_layout
    nx.draw(G, graphviz_layout(G))
