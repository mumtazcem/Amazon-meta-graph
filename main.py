import pandas as pd
import numpy as np
import networkx as nx
import project_view as pv
import networkx.algorithms.community as nx_comm
import random
import time

# Seed value for betweenness centrality and for random choices
seed = 900

# Most Crowded Modules would be saved to..
g1_modules_file = "most_crowded_modules/g1_modules.csv"
g2_modules_file = "most_crowded_modules/g2_modules.csv"

# Page Ranks would be saved to..
g1_pagerank_file = "page_ranks/g1_pagerank_file.csv"
g2_pagerank_file = "page_ranks/g2_pagerank_file.csv"

# Database
g1_pd = "saved_dataframes/g1Db_clean.csv"
g2_pd = "saved_dataframes/g2Db_clean.csv"
g1_db = pd.read_csv(g1_pd)
g2_db = pd.read_csv(g2_pd)

# Fix nodeId column
num_of_nodes1, col1 = g1_db.shape
g1_db['nodeId'] = np.full((num_of_nodes1,), range(num_of_nodes1))
num_of_nodes2, col2 = g2_db.shape
g2_db['nodeId'] = np.full((num_of_nodes2,), range(num_of_nodes2))


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

    num_of_nodes, num_of_edges = pv.get_nodes_and_edges_number(G1)
    print("Number of nodes :", num_of_nodes, "number of edges :", num_of_edges)
    # pv.plot_degree_dist(G1)

    num_of_nodes, num_of_edges = pv.get_nodes_and_edges_number(G2)
    print("Number of nodes :", num_of_nodes, "number of edges :", num_of_edges)
    # pv.plot_degree_dist(G2)
    return G1, G2


# Modified Girvan-Newman algorithm from HW3
def modified_girvan_newman_algorithm(g):
    initial = nx_comm.modularity(g, [set(g.nodes)], weight='weight')
    max_modularity = initial
    saved_components = []
    saved_graph = nx.Graph()
    while g.number_of_edges() != 0:
        centralities = nx.edge_betweenness_centrality(g, weight='weight', seed=seed)
        # max() returns one of the edges with maximum centrality
        u, v = max(centralities, key=centralities.get)
        # Checking for same maximum centrality score below
        if len(sorted(centralities.values(), reverse=True)) > 2:
            centrality_max1 = sorted(centralities.values(), reverse=True)[0]
            centrality_max2 = sorted(centralities.values(), reverse=True)[1]
            if centrality_max1 == centrality_max2:
                # At least two equal max centrality measure detected!
                same_scores = []
                for centrality in centralities:
                    if centralities[centrality] == centrality_max1:
                        same_scores.append(centrality)
                # Pick an edge randomly among same scores
                u, v = random.Random(seed).choice(same_scores)
        # same score check finishes.
        components = sorted(nx.connected_components(g), key=len, reverse=True)
        if len(components) > 1:
            fragmented_modularity = nx_comm.modularity(g, components, weight='weight')
            if fragmented_modularity > max_modularity:
                max_modularity = fragmented_modularity
                saved_components = components
                saved_graph = g.copy()
        g.remove_edge(u, v)
    return max_modularity, saved_components, saved_graph


def most_crowded_module(all_components):
    max_len = 0
    most_crowded_modules = []
    for component in all_components:
        if max_len < len(component):
            max_len = len(component)
    for component in all_components:
        if max_len == len(component):
            most_crowded_modules.append(component)
    return max_len, most_crowded_modules


# Gets two graphs, runs Girvan Newman algorithm
# Finds connected components. Among connected components,
# it would print out the most crowded connected components
# to csv files under most_crowded_modules folder.
def modularity_calculations(G1, G2, filename1, filename2):
    start_time = time.time()
    print("******   Modularity Calculation Started   ******")
    print("Running G1")
    result_modularity, g1_result_components, result_graph = modified_girvan_newman_algorithm(G1)
    print("Final modularity: ", result_modularity)
    print("Connected components of the graph with maximum modularity: ", g1_result_components)
    g1_max_len, g1_most_crowded_modules = most_crowded_module(g1_result_components)
    print("most_crowded_module include : ", g1_max_len, " nodes.")
    print("most_crowded_modules: ", g1_most_crowded_modules)
    # pv.draw_networkx_graph(result_graph)

    g1_time = time.time()
    print("G1 modularity is finished in --- %s seconds ---" % (g1_time - start_time))

    print("Running G2")
    result_modularity, g2_result_components, result_graph = modified_girvan_newman_algorithm(G2)
    print("Final modularity: ", result_modularity)
    print("Connected components of the graph with maximum modularity: ", g2_result_components)
    g2_max_len, g2_most_crowded_modules = most_crowded_module(g2_result_components)
    print("most_crowded_module include : ", g2_max_len, " nodes.")
    print("most_crowded_modules: ", g2_most_crowded_modules)
    # pv.draw_networkx_graph(result_graph)

    g2_time = time.time()
    print("G2 is finished --- %s seconds ---" % (g2_time - g1_time))
    print("Modularity finished in %s seconds." % (time.time() - start_time))
    print("******   Modularity Calculation Ended   ******")

    print("Printing modules of G1..")
    g1_modules_asin = []
    for module_ in g1_result_components:
        module_asin = []
        for product in module_:
            module = g1_db[g1_db['nodeId'] == product]
            module_asin.append(module['ASIN'].iat[0])
        g1_modules_asin.append(module_asin)
    df1 = pd.DataFrame(g1_modules_asin)

    # the number of nodes in the corresponding module
    df1['NumberOfNodes'] = ""
    for row_index, row in df1.iterrows():
        node_counter = 0
        for column in row:
            if column is not None:
                node_counter += 1
        df1.at[row_index, 'NumberOfNodes'] = node_counter - 1
    with open(filename1, 'w', newline='') as myfile:
        df1.to_csv(filename1)

    print("Printing modules of G2..")
    g2_modules_asin = []
    for module_ in g2_result_components:
        module_asin = []
        for product in module_:
            module = g2_db[g2_db['nodeId'] == product]
            module_asin.append(module['ASIN'].iat[0])
        g2_modules_asin.append(module_asin)
    df2 = pd.DataFrame(g2_modules_asin)
    # the number of nodes in the corresponding module
    df2['NumberOfNodes'] = ""
    for row_index, row in df2.iterrows():
        node_counter = 0
        for column in row:
            if column is not None:
                node_counter += 1
        df2.at[row_index, 'NumberOfNodes'] = node_counter - 1  # minus 1 because of NumberOfNodes column
    with open(filename2, 'w', newline='') as myfile:
        df2.to_csv(filename2)
    return df1, df2


def page_rank_calculations(G1, G2):
    # G1
    pr = nx.pagerank(G1, alpha=0.9, max_iter=1000, weight='weight')
    sorted_pr = {k: v for k, v in sorted(pr.items(), key=lambda item: item[1], reverse=True)}
    # print(sorted_pr)
    g1_pr_df = pd.DataFrame.from_dict(sorted_pr, orient='index')
    g1_pr_df["ASIN"] = ""
    for index, row in g1_pr_df.iterrows():
        product = g1_db[g1_db['nodeId'] == index]
        g1_pr_df.at[index, 'ASIN'] = product['ASIN'].iat[0]

    # G2
    pr = nx.pagerank(G2, alpha=0.9, max_iter=1000, weight='weight')
    sorted_pr = {k: v for k, v in sorted(pr.items(), key=lambda item: item[1], reverse=True)}
    # print(sorted_pr)
    g2_pr_df = pd.DataFrame.from_dict(sorted_pr, orient='index')
    g2_pr_df["ASIN"] = ""
    for index, row in g2_pr_df.iterrows():
        product = g2_db[g2_db['nodeId'] == index]
        g2_pr_df.at[index, 'ASIN'] = product['ASIN'].iat[0]
    return g1_pr_df, g2_pr_df


# Searches over modules, finds the corresponding module for the input ASIN
def search_modules(modules_dataframe, input_asin):
    for index, row in modules_dataframe.iterrows():
        for column_asin in row:
            if column_asin == input_asin:
                return index, modules_dataframe.at[index, 'NumberOfNodes']


# Given pagerank and modularity, this method would create the R space that includes
# node's
# ID
# PageRank
# ASIN
# Module degree
# Module that it belongs to
def create_relationship_space(graph_pagerank, graph_modularity):
    # Add module degree column. Module degree represents the number of nodes in the module that this node belongs to
    graph_pagerank["ModuleDegree"] = ""
    # Given pagerank find its corresponding module ID that this node belongs to
    graph_pagerank["BelongsTo"] = ""
    for index, row in graph_pagerank.iterrows():
        product_asin = graph_pagerank.at[index, 'ASIN']
        # search over modules
        module_index, module_degree = search_modules(graph_modularity, product_asin)
        graph_pagerank.at[index, 'BelongsTo'] = module_index
        graph_pagerank.at[index, 'ModuleDegree'] = module_degree

    return graph_pagerank


# Calculate pagerank sum of the most popular module and return the module degree of the graph
def morphospace_values(graph_pagerank, graph_modularity, is_reading_from_file):
    sum_pagerank = 0
    for i in range(len(graph_modularity.columns) - 2):
        if is_reading_from_file:
            product_asin = graph_modularity.at[0, str(i)]
        else:
            product_asin = graph_modularity.at[0, i]
        # For file reading, use this below
        # product_asin = graph_modularity.at[0, str(i)]
        # graph_modularity.loc[graph_modularity.index[0], 6]
        # get its pagerank
        for index, row in graph_pagerank.iterrows():
            if product_asin == row['ASIN']:
                # 0 is the column name unfortunately for the pagerank
                if is_reading_from_file:
                    sum_pagerank += row['0']
                else:
                    sum_pagerank += row[0]
                break
    return sum_pagerank, graph_modularity.at[0, 'NumberOfNodes']


def do_calculations_using_file(file1_pr, file2_pr, file1_mod, file2_mod):
    g1_pagerank = pd.read_csv(file1_pr)
    g2_pagerank = pd.read_csv(file2_pr)
    g1_modularity = pd.read_csv(file1_mod)
    g2_modularity = pd.read_csv(file2_mod)

    # Get morphospace values for graphs
    sum_page_rank1, mod_degree1 = morphospace_values(g1_pagerank, g1_modularity, is_reading_from_file=True)
    sum_page_rank2, mod_degree2 = morphospace_values(g2_pagerank, g2_modularity, is_reading_from_file=True)
    print(sum_page_rank1)
    print(mod_degree1)
    print(sum_page_rank2)
    print(mod_degree2)
    return sum_page_rank1, mod_degree1, sum_page_rank2, mod_degree2


# Provide file names to be written to
def do_all_calculations(G1, G2, file_mod1, file_mod2, file_pr1, file_pr2):
    # Calculate pagerank and modules
    g1_pagerank, g2_pagerank = page_rank_calculations(G1, G2)
    g1_modularity, g2_modularity = modularity_calculations(G1, G2, file_mod1, file_mod2)

    # Create the R space
    g1_relationship = create_relationship_space(g1_pagerank, g1_modularity)
    g2_relationship = create_relationship_space(g2_pagerank, g2_modularity)
    # Get morphospace values for graphs
    sum_page_rank1, mod_degree1 = morphospace_values(g1_pagerank, g1_modularity, is_reading_from_file=False)
    sum_page_rank2, mod_degree2 = morphospace_values(g2_pagerank, g2_modularity, is_reading_from_file=False)
    print(sum_page_rank1)
    print(mod_degree1)
    print(sum_page_rank2)
    print(mod_degree2)
    # Write to a file
    with open(file_pr1, 'w', newline='') as myfile:
        g1_relationship.to_csv(g1_pagerank_file)
    with open(file_pr2, 'w', newline='') as myfile:
        g2_relationship.to_csv(g2_pagerank_file)


# Generate real G1 G2
G1, G2 = generate_g1_g2()
do_all_calculations(G1, G2, g1_modules_file, g2_modules_file, g1_pagerank_file, g2_pagerank_file)
do_calculations_using_file(g1_pagerank_file, g2_pagerank_file, g1_modules_file, g2_modules_file)

