# Marcin Damek, M.Cem Eriş, Mehmet Sezer, Recep O. Yıldız
# {damek20, erismu, sezer20, yildizr} @itu.edu.tr
# ITU BLG 549E Graph Theory and Algorithms
# Project
# Reference Metadata: https://snap.stanford.edu/data/amazon-meta.html
# Visualization of Graphs and Adjacency Matrices

# TODO Merge with project.py after all done.

import networkx as nx
import matplotlib.pyplot as plt
import random


def er_random_graph_generator(n, p, ng, seed, w_base, w_top):
    """Returns Erdos Renyi Graphs.

        Parameters
        ----------
        n : int
            The number of nodes.
        p : float
            The probability of adding a new edge for each edge.
        ng : int
            The number of graphs.
        seed : int
            The seed for the random number generator.
        w_base : int
            The base value for edge weight.
        w_top : int
            The maximum value for edge weight.

        Returns
        -------
        Erdos Renyi Graphs.

        Notes
        -----
        Note that the seed is increased in every step of for loop.
        """

    f_er_graph_list = []
    for i in range(0, ng):
        f_g = nx.erdos_renyi_graph(n, p, seed + i, directed=False)
        for (u, v, w) in f_g.edges(data=True):
            w['weight'] = random.randint(w_base, w_top)
        f_er_graph_list.append(f_g)
    return f_er_graph_list


def test_project_view():
    n = 1000
    p = 0.4
    ng = 1
    seed = 2021
    w_base = 0
    w_top = 1024

    er_graph_list = er_random_graph_generator(n, p, ng, seed, w_base, w_top)

    plt.figure(num=None, figsize=(15, 15), dpi=100, facecolor='#FFCC66')
    plt.axis('off')
    nx.draw_networkx(er_graph_list[0])
    plt.title("NetworkData")
    plt.show()

def draw_networkx_graph(G):    
    pos=nx.spring_layout(G)
    nx.draw_networkx(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()
    
convert_graph_to_adjecency_matrix = lambda G: nx.to_numpy_matrix(G)

convert_adjecency_matrix_to_graph = lambda adjecency_matrix: nx.from_numpy_matrix(adjecency_matrix)
    
def show_adjacency_matrix_from_graph(G):
    adjacency_matrix = convert_graph_to_adjecency_matrix(G)
    plt.imshow(adjacency_matrix)
    plt.colorbar()
    plt.title("Adjacency matrix")
    plt.show()
    
def show_adjacency_matrix(adjacency_matrix):
    plt.imshow(adjacency_matrix)
    plt.colorbar()
    plt.title("Adjacency matrix")
    plt.show()
    
def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.xlabel("degree")
    plt.ylabel("count")
    plt.title("Degree histogram")
    plt.show()

def get_nodes_and_edges_number(G):
    return (G.number_of_nodes(), G.number_of_edges())

# test_project_view()
