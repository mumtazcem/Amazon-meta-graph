import random

def randomize_graphs(G, number_of_new_graphs):
    new_graphs = []
    for graph_number in range(number_of_new_graphs):
        tmp_graph = G.copy()
        nodes_number = tmp_graph.number_of_nodes()
        for i in range (nodes_number):
            # container for selected randomly, two existing, different edges
            selectedEdges = []
            while len(selectedEdges) < 2:
                firstPartEdge = random.randrange(0, nodes_number - 1)
                secondPartEdge = random.randrange(0, nodes_number - 1)
                #checking if edge exist and if is not in selectdEdges
                if tmp_graph.has_edge(firstPartEdge, secondPartEdge) and (firstPartEdge, secondPartEdge) not in selectedEdges and (secondPartEdge, firstPartEdge) not in selectedEdges:
                    selectedEdges.append((firstPartEdge, secondPartEdge))
            #check if new connection exist. If exist, skip and go to random new pair
            if tmp_graph.has_edge(selectedEdges[0][0], selectedEdges[1][1]) or  tmp_graph.has_edge(selectedEdges[1][0],selectedEdges[0][1]):
                selectedEdges.clear()
                continue
            edge_0_weight = tmp_graph.get_edge_data(*selectedEdges[0])['weight']
            edge_1_weight = tmp_graph.get_edge_data(*selectedEdges[1])['weight']
            # remove edge for swap start and end point in edge
            tmp_graph.remove_edge(*selectedEdges[0])
            tmp_graph.remove_edge(*selectedEdges[1])
            # add new changed edges
            tmp_graph.add_edge(selectedEdges[0][0],selectedEdges[1][1],  weight=edge_0_weight)
            tmp_graph.add_edge(selectedEdges[1][0],selectedEdges[0][1],  weight=edge_1_weight)
            selectedEdges.clear()
        new_graphs.append(tmp_graph)
    return new_graphs