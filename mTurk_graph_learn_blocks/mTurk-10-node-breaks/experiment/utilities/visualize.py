import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def animate_walk(G, walk):
    """
    Takes a graph and walk and creates an animation that can
    be saved to a movie

    e.g.
    anim.save(filename.mp4, writer='ffmpeg', fps=15, dpi=dpi)
    """
    fig = plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G)
    nc = np.ones(15)
    nodes = nx.draw_networkx_nodes(G, pos, node_color=nc)
    edges = nx.draw_networkx_edges(G, pos)

    def update(n):
        nc = np.ones(15)
        # nc = np.random.random(15)
        nc[walk[n]] = 0
        nodes.set_array(nc)
        return nodes,

    anim = FuncAnimation(fig, update, frames=len(walk),
                         interval=500, blit=True)
    plt.close()
    return anim
