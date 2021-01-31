import pandas as pd
import numpy as np
import networkx as nx
import project_view as pv
import time

start_time = time.time()
print("Started...")

# to be read from
g1_file = "saved_dataframes/g1Db_clean.csv"
g2_file = "saved_dataframes/g2Db_clean.csv"

# to be written to
adj1_file = "saved_adj_matrices/adj1_full.csv"
adj2_file = "saved_adj_matrices/adj2_full.csv"

g1 = pd.read_csv(g1_file)
g2 = pd.read_csv(g2_file)

# filter out nodes below threshold, because it takes a lot of time. 3000 finishes fast
# threshold = 3000
# g1 = g1[g1['nodeId'] < threshold]
# g2 = g2[g2['nodeId'] < threshold]

n1, col1 = g1.shape
n2, col2 = g2.shape

adj_1 = np.zeros((n1, n1), dtype=int)
adj_2 = np.zeros((n2, n2), dtype=int)

run_G1 = True
run_G2 = True

if run_G1:
    print("Running G1")
    idDict = {}
    j = 0
    for i in g1['Id']:
        idDict[i] = j
        j = j +1
    for index, row in g1.iterrows():
        for i in range(5):
            # similarity_indices: s1, s2, s3, s4 ,s5
            similarity_index = "s" + str(i + 1)
            vote_index = "v" + str(i + 1)
            similar_product_asin = row[similarity_index]
            # if the similar cell is null
            if np.isnan(row[similarity_index]):
                continue
            # if no weight is assigned
            x = idDict.get(row['Id'])
            y = idDict.get(row[similarity_index])
            if adj_1[x][y] == 0:
                # sum both products' totalVote values
                weight = row['totalVote'] + row[vote_index]
                # assign the weight to the corresponding spot
                adj_1[x][y] = weight

    G1 = nx.from_numpy_matrix(adj_1)
    num_of_nodes, num_of_edges = pv.get_nodes_and_edges_number(G1)
    print("Number of nodes :", num_of_nodes, "number of edges :", num_of_edges)
    pd.DataFrame(adj_1).to_csv(adj1_file)
    # pv.show_adjacency_matrix(adj_1)
    # pv.show_adjacency_matrix_from_graph(G1)
    # pv.draw_networkx_graph(G1)
    pv.plot_degree_dist(G1)

g1_time = time.time()
print("G1 is finished in --- %s seconds ---" % (g1_time - start_time))


if run_G2:
    print("Running G2")
    idDict = {}
    j = 0
    for i in g2['Id']:
        idDict[i] = j
        j = j +1
    for index, row in g2.iterrows():
       for i in range(5):
            # similarity_indices: s1, s2, s3, s4 ,s5
            similarity_index = "s" + str(i + 1)
            vote_index = "v" + str(i + 1)
            similar_product_asin = row[similarity_index]
            # if the similar cell is null
            if np.isnan(row[similarity_index]):
                continue
            x = idDict.get(row['Id'])
            y = idDict.get(row[similarity_index])
            if adj_2[x][y] == 0:
                # sum both products' totalVote values
                weight = row['totalVote'] + row[vote_index]
                # assign the weight to the corresponding spot
                adj_2[x][y] = weight
                #print(weight)

    G2 = nx.from_numpy_matrix(adj_2)
    num_of_nodes, num_of_edges = pv.get_nodes_and_edges_number(G2)
    print("Number of nodes :", num_of_nodes, "number of edges :", num_of_edges)
    pd.DataFrame(adj_2).to_csv(adj2_file)
    # pv.show_adjacency_matrix(adj_2)
    # pv.show_adjacency_matrix_from_graph(G2)
    # pv.draw_networkx_graph(G2)

g2_time = time.time()
print("G2 is finished --- %s seconds ---" % (g2_time - g1_time))

pv.plot_degree_dist(G2)


print("All finished in %s seconds." % (time.time() - start_time))
