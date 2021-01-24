import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def main():

    product={}
    productList =[]
    similarProduct = {}
    similarityLabel = ['totalSimilar', 's1', 's2', 's3', 's4', 's5']
    totalReview = 0
    reviewCounter = 0
    voteCounter = 0

    dataFrameType = 1               # 1 : one dataframe; 2 : two dataframe
    selectedGroup1 = 'Video'
    selectedGroup2 = 'Music'

    g1IdList = []                       # ID of selectedGroup1 products
    g1PrList = []
    g2IdList = []                       # ID of selectedGroup2 products
    g2PrList = []

    # Read all lines of the meta data into content list.
    file_name = "amazon_first_100_mod.txt"
    #file_name = "deneme.txt"
    with open(file_name, encoding='utf8') as f:
        content = f.readlines()
    # Remove the beginning and trailing white spaces.
    content = [x.strip() for x in content]
    for line in content:
    
        parser_colon = line.split(':')
        parser_space = line.split()

        if  len(parser_colon) > 1 and parser_space[0] != 'Total':
            if parser_colon[0] != 'categories' and parser_colon[0] != 'title':
                    
                if parser_colon[0] == 'similar':
                    similarityLine=parser_colon[1].split(' ')
                    similarityLine=list(filter(None, similarityLine))
                    while len(similarityLine) != 6:
                        similarityLine.append(None)         # add none if there are less then 5 similar items
                    similarProduct[product['Id']] = similarityLine
                    product = {**product, **dict(zip(similarityLabel, similarityLine))}
                    
                elif parser_colon[0] == 'reviews' and parser_colon[1].strip() == 'total': 
                        product['totalReview']  = parser_colon[2].split(' ')[1]
                        product['avgRate']  = parser_colon[4].strip()
                        totalReview = int(product['totalReview'] )
                        if totalReview == 0:
                            product['totalVote'] = 0
                            productList.append(product)
                            product={}
                
                elif reviewCounter < totalReview:
                    if parser_space[1] == "cutomer:":
                        reviewCounter = reviewCounter +1
                        voteCounter = voteCounter + int(parser_space[6])
                        if reviewCounter == totalReview:
                            product['totalVote'] = voteCounter
                            voteCounter = 0
                            totalReview = 0
                            reviewCounter = 0
                            productList.append(product)
                            product={}
                            
                else:
                    product[parser_colon[0]]  = parser_colon[1].strip() 
                    
                    if parser_colon[0] == "group":
                        currentGroup = product['group']
                        if currentGroup == selectedGroup1:
                            g1IdList.append(product['Id'])
                        elif currentGroup == selectedGroup2:
                            g2IdList.append(product['Id'])

    g1Counter = 0
    for pr in productList:
        if pr['Id'] == g1IdList[g1Counter]:
            g1PrList.append(pr)
            g1Counter = g1Counter + 1
            if g1Counter == len(g1IdList):
                break
            
    g2Counter = 0
    for pr in productList:
        if pr['Id'] == g2IdList[g2Counter]:
            g2PrList.append(pr)
            g2Counter = g2Counter + 1
            if g2Counter == len(g2IdList):
                break
                
    """            
    dataset = pd.DataFrame.from_dict(productList)
    dataset.to_csv("database.csv")

    if dataFrameType == 1:
        g1g2Db = pd.concat([g1Db,g2Db])
        g1g2Db.to_csv("g1g2Db.csv")  
    else:
    """

    g1Db= pd.DataFrame.from_dict(g1PrList)
    g1Db.to_csv("g1Db.csv")

    g2Db = pd.DataFrame.from_dict(g2PrList)
    g2Db.to_csv("g2Db.csv")    
    
    
    g1 = nx.DiGraph()
    g1Asin = g1Db['ASIN'].tolist()
    g1.add_nodes_from(g1Asin)
    for pr in g1PrList:
        for simIndex in range (int(pr['totalSimilar'])):
            g1.add_edge(pr['ASIN'], pr[similarityLabel[simIndex + 1]])
    print(g1.number_of_nodes(), g1.number_of_edges())

    plt.figure()
    nx.draw(g1)  # networkx draw()
    plt.savefig("g1.png")     
    
    g2 = nx.DiGraph()
    g2Asin = g2Db['ASIN'].tolist()
    g2.add_nodes_from(g2Asin)
    for pr in g2PrList:
        for simIndex in range (int(pr['totalSimilar'])):
            g2.add_edge(pr['ASIN'], pr[similarityLabel[simIndex + 1]])
    print(g2.number_of_nodes(), g2.number_of_edges())
    
    plt.figure()
    nx.draw(g2)  # networkx draw()
    plt.savefig("g2.png")     
    
    
    
if __name__ == "__main__":
    main()