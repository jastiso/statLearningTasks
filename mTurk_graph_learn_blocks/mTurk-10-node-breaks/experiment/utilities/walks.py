import random
import networkx as nx
import numpy as np
from utilities import graphs

random.seed()

modular_jumps = {
    0: [5, 10],
    1: [6, 7, 8, 11, 12, 13],
    2: [6, 7, 8, 11, 12, 13],
    3: [6, 7, 8, 11, 12, 13],
    4: [9, 14],
    5: [0, 10],
    6: [1, 2, 3, 11, 12, 13],
    7: [1, 2, 3, 11, 12, 13],
    8: [1, 2, 3, 11, 12, 13],
    9: [4, 14],
    10: [0, 5],
    11: [1, 2, 3, 6, 7, 8],
    12: [1, 2, 3, 6, 7, 8],
    13: [1, 2, 3, 6, 7, 8],
    14: [4, 9]}

########
# WALKS
########


def random_walk(G, n):
    node = random.choice(list(G.nodes()))
    walk = [node]
    for i in range(n - 1):
        node = random.choice(list(G[node].keys()))
        walk.append(node)
    return walk

def hamiltonian_walk(n):
    """
    Generates a hamiltonian walk for the modular graph
    """
    def make_single_traversal(starting_node, reverse):
        traversal = [0]

        block = [1,2,3]
        random.shuffle(block)
        traversal += block
        traversal += [4,5]

        block = [6,7,8]
        random.shuffle(block)
        traversal += block
        traversal += [9]
        #
        #block = [11,12,13]
        #random.shuffle(block)
        #traversal += block
        #traversal += [14]

        # reverse traversal
        if reverse:
            traversal = traversal[::-1]

        # set a non-zero starting node
        ind = np.where([x == starting_node for x in traversal])[0][0]
        traversal = traversal[ind:] + traversal[:ind]

        return traversal

    reverse = random.choice([True, False])
    starting_node = random.choice(range(10))
    walk = make_single_traversal(starting_node, reverse)

    while len(walk) < n:
        current_node = walk[-1]
        reverse = random.choice([True, False])
        next_node = random.choice(graphs.modular[current_node].keys())
        walk.extend(make_single_traversal(next_node, reverse))

    return walk[:n]

def find_valid_jumps(G):
    """
    Given a graph, return a dictionary of nodes,
    listing all nodes at least 3 nodes away from that node
    """
    path_lengths = nx.shortest_paths.shortest_path_length(G)
    valid_jumps = {}
    for n, dists in path_lengths:
        valid_jumps[n] = [k for k, v in dists.items() if v == 3]
    return valid_jumps


def random_walk_with_jumps(G, n_steps, n_jumps, min_dist=10, valid_jumps=None):
    """
    Generate <n_jumps> blocks of at least <min_dist + 1> connected nodes.

    Each block begins with a jump, and then the remaining <min_dist> nodes
    are all sequential.

    Blocks all begin at <min_dist + 1> length, and remaining steps in the walk
    are randomly added on.
    """
    spaces = np.ones(n_jumps, dtype=np.int) * (min_dist + 1)  # jump + <min_dist> correct transitions
    spaces = np.append(spaces, 1)  # Need to have a block of at least one node (the jump itself)
    remaining_nodes = n_steps - np.sum(spaces)

    if not valid_jumps:
        valid_jumps = find_valid_jumps(G)

    if remaining_nodes < 0:
        raise ValueError('Invalid input combination: not enough nodes')

    for i in range(remaining_nodes):
        x = np.random.choice(range(len(spaces)))
        spaces[x] += 1

    node = random.choice(G.nodes().keys())
    walk = [node]
    is_jump = [False]
    for i, block_length in enumerate(spaces):
        if i > 0:
            node = random.choice(valid_jumps[node])
            walk.append(node)
            is_jump.append(True)
        for j in range(block_length - 1):
            node = random.choice(G[node].keys())
            walk.append(node)
            is_jump.append(False)
    return (walk, is_jump)


def get_jump_distribution(jumps):
    from collections import Counter
    idx = np.where(jumps)[0]
    return Counter(idx[1:] - idx[:-1])


def plot_distribution(jumps):
    import matplotlib.pyplot as plt
    dist = get_jump_distribution(jumps)
    vals = np.zeros(np.max(dist.keys()) + 1)
    for k, v in dist.iteritems():
        vals[k] = v
    plt.plot(vals)
    plt.show()


# def std_walk_with_jumps():
#     G = generate_random_graphs(100)
#     G = representative_graphs(G)
#     G = random.choice(G)
#     return walk_with_jumps(G, 1400, 40)


# def choose_random_graph():
#     graphs = representative_graphs(1000)
#     G = random.choice(graphs)
#     return G
