# Marcin Damek, M.Cem Eriş, Mehmet Sezer, Recep O. Yıldız
# {damek20, erismu, sezer20, yildizr} @itu.edu.tr
# ITU BLG 549E Graph Theory and Algorithms
# Project
# Reference Metadata: https://snap.stanford.edu/data/amazon-meta.html
# Visualization of Graphs and Adjacency Matrices

import networkx as nx
import matplotlib.pyplot as plt
import random
from datetime import datetime
import os
from collections import OrderedDict, Counter
import pandas as pd


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
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


convert_graph_to_adjecency_matrix = lambda G: nx.to_numpy_matrix(G)

convert_adjecency_matrix_to_graph = lambda adjecency_matrix: nx.from_numpy_matrix(adjecency_matrix)


def create_directory_if_not_exist(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def show_adjacency_matrix_from_graph(G):
    adjacency_matrix = convert_graph_to_adjecency_matrix(G)
    plt.imshow(adjacency_matrix, cmap=plt.get_cmap('binary'))
    plt.colorbar()
    plt.title("Adjacency matrix")
    create_directory_if_not_exist('figures')
    plt.savefig('figures/adjacency_matrix_' + datetime.now().strftime("%H_%M_%S") + '.png')
    plt.show()


def show_adjacency_matrix(adjacency_matrix):
    plt.imshow(adjacency_matrix, cmap=plt.get_cmap('binary'))
    plt.colorbar()
    plt.title("Adjacency matrix")
    create_directory_if_not_exist('figures')
    plt.savefig('figures/adjacency_matrix_' + datetime.now().strftime("%H_%M_%S") + '.png')
    plt.show()


def plot_strength_distribution(G):
    nodes_with_weights = G.degree(weight='weight')
    ids = list(map(lambda x: x[0], nodes_with_weights))
    values = list(map(lambda x: x[1], nodes_with_weights))
    plt.bar(ids, values)
    plt.show()


def plot_differences_with_strenght_distribution(G1, G2, in_one):
    nodes_with_weights1 = G1.degree(weight='weight')
    ids1 = list(map(lambda x: x[0], nodes_with_weights1))
    values1 = list(map(lambda x: x[1], nodes_with_weights1))
    nodes_with_weights2 = G2.degree(weight='weight')
    ids2 = list(map(lambda x: x[0], nodes_with_weights2))
    values2 = list(map(lambda x: x[1], nodes_with_weights2))
    if in_one:
        plt.title("Strength distributions of graphs")
        plt.bar(ids1, values1)
        plt.bar(ids2, values2)
        plt.show()
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.suptitle("Strength distributions of graphs")
        ax1.bar(ids1, values1)
        ax2.bar(ids2, values2)
        plt.show()


def plot_degree_dist(G):
    degrees = dict(Counter(list(map(lambda x: G.degree(x), G.nodes()))))
    degrees = OrderedDict(sorted(degrees.items()))
    plt.figure(figsize=(15, 10))
    keys = list(map(lambda x: str(x), degrees.keys()))
    plt.bar(keys, degrees.values())
    for a, b in enumerate(degrees.values()):
        plt.text(a, b, str(b), horizontalalignment='center')
    plt.xlabel("degree")
    plt.ylabel("count")
    plt.title("Degree histogram")
    create_directory_if_not_exist('figures')
    plt.savefig('figures/histogram_' + datetime.now().strftime("%H_%M_%S") + '.png')
    plt.show()


# This is the method to create the degree distributions of both G1 and G2
# in an overlaid manner.
def plot_degree_dist_combined(G1, G2):
    width = 0.8
    degrees1 = dict(Counter(list(map(lambda x: G1.degree(x), G1.nodes()))))
    degrees1 = OrderedDict(sorted(degrees1.items()))
    keys1 = list(map(lambda x: str(x), degrees1.keys()))
    degrees2 = dict(Counter(list(map(lambda x: G2.degree(x), G2.nodes()))))
    degrees2 = OrderedDict(sorted(degrees2.items()))
    keys2 = list(map(lambda x: str(x), degrees2.keys()))
    plt.xlabel("degree")
    plt.ylabel("count")
    plt.title("Degree distributions of graphs G1 (Video), and G2 (DVD)")
    plt.bar(keys1, degrees1.values(), width=width,
            color='b', label='G1 (Video)')
    plt.bar(keys2, degrees2.values(), color='r', width=0.5 * width, alpha=0.5, label='G2 (DVD)')
    # width = 0.5 * width
    plt.legend()
    plt.savefig('figures/g1_g2_distr_overlaid.png')
    plt.show()


def get_nodes_and_edges_number(G):
    return (G.number_of_nodes(), G.number_of_edges())


# test_project_view()

def generate_g1_g2():
    # Thresholded
    adj1_file = "saved_adj_matrices/adj1_min.csv"
    adj2_file = "saved_adj_matrices/adj2_min.csv"

    adj_1_pd = pd.read_csv(adj1_file)
    adj_2_pd = pd.read_csv(adj2_file)

    # need to drop index column that is generated by pandas
    adj_1_pd.drop(adj_1_pd.columns[0], axis=1, inplace=True)
    adj_2_pd.drop(adj_2_pd.columns[0], axis=1, inplace=True)

    # convert pd to numpy
    adj_1 = adj_1_pd.to_numpy()
    adj_2 = adj_2_pd.to_numpy()

    # generate nx graphs from adj matrices
    G1 = nx.from_numpy_matrix(adj_1)
    G2 = nx.from_numpy_matrix(adj_2)

    num_of_nodes, num_of_edges = get_nodes_and_edges_number(G1)
    print("Number of nodes :", num_of_nodes, "number of edges :", num_of_edges)

    num_of_nodes, num_of_edges = get_nodes_and_edges_number(G2)
    print("Number of nodes :", num_of_nodes, "number of edges :", num_of_edges)
    plot_degree_dist_combined(G1, G2)
    return G1, G2


# G1, G2 = generate_g1_g2()
# plot_degree_dist_combined(G1, G2)
