import pandas as pd
import time

start_time = time.time()
print("Started...")

g1_file = "saved_dataframes/g1Db.csv"
g2_file = "saved_dataframes/g2Db.csv"
g1_clean = "saved_dataframes/g1Db_clean.csv"
g2_clean = "saved_dataframes/g2Db_clean.csv"

g1 = pd.read_csv(g1_file)
g2 = pd.read_csv(g2_file)

n1, col1 = g1.shape
n2, col2 = g2.shape

run_G1 = True
run_G2 = True

g1 = g1.drop('Unnamed: 0', axis=1)
g2 = g2.drop('Unnamed: 0', axis=1)

if run_G1:
    print("Running G1")
    g1['visited'] = 0
    for index, row in g1.iterrows():
        removeS = []
        for j in range(5):
            vote_index = "v" + str(j + 1)
            g1.at[index, vote_index] = 0
        for i in range(row['totalSimilar']):
            # similarity_indices: s1, s2, s3, s4 ,s5
            similarity_index = "s" + str(i + 1)
            similar_product_asin = row[similarity_index]
            # if the similar cell is null
            if isinstance(row[similarity_index], float):
                continue
            similar_product_row = g1[g1['ASIN'].str.contains(similar_product_asin)]
            if similar_product_row['ASIN'].empty:
                removeS.append(similarity_index)
            else:
                vote_index = "v" + str(i + 1)
                visitedIndex = list(similar_product_row['visited'].to_dict())[0]
                g1.at[visitedIndex, 'visited'] = g1.at[visitedIndex, 'visited'] + 1
                g1.at[index, 'visited'] = g1.at[index, 'visited'] + 1
                g1.at[index, similarity_index] = int(similar_product_row['Id'])
                g1.at[index, vote_index] = int(similar_product_row['totalVote'])

        totalSimilar = row['totalSimilar'] - len(removeS)
        g1.at[index, 'totalSimilar'] = row['totalSimilar'] - len(removeS)
        for s in (removeS):
            g1.at[index, s] = None

    for index, row in g1.iterrows():
        if row['totalSimilar'] == 0 and g1.at[index, 'visited'] == 0:
            g1.drop(index, inplace=True)

    with open(g1_clean, 'w', newline='') as myfile:
        g1.to_csv(g1_clean)

g1_time = time.time()
print("G1 is finished in --- %s seconds ---" % (g1_time - start_time))

if run_G2:
    print("Running G2")
    g2['visited'] = 0
    for index, row in g2.iterrows():
        removeS = []
        for j in range(5):
            vote_index = "v" + str(j + 1)
            g2.at[index, vote_index] = None

        for i in range(row['totalSimilar']):
            # similarity_indices: s1, s2, s3, s4 ,s5
            similarity_index = "s" + str(i + 1)
            similar_product_asin = row[similarity_index]
            # if the similar cell is null
            if isinstance(row[similarity_index], float):
                continue
            similar_product_row = g2[g2['ASIN'].str.contains(similar_product_asin)]
            if similar_product_row['ASIN'].empty:
                removeS.append(similarity_index)
            else:
                vote_index = "v" + str(i + 1)
                visitedIndex = list(similar_product_row['visited'].to_dict())[0]
                g2.at[visitedIndex, 'visited'] = g2.at[visitedIndex, 'visited'] + 1
                g2.at[index, 'visited'] = g2.at[index, 'visited'] + 1
                g2.at[index, similarity_index] = int(similar_product_row['Id'])
                g2.at[index, vote_index] = int(similar_product_row['totalVote'])

        totalSimilar = row['totalSimilar'] - len(removeS)
        g2.at[index, 'totalSimilar'] = totalSimilar
        for s in (removeS):
            g2.at[index, s] = None

    for index, row in g2.iterrows():
        if row['totalSimilar'] == 0 and g2.at[index, 'visited'] == 0:
            g2.drop(index, inplace=True)

    with open(g2_clean, 'w', newline='') as myfile:
        g2.to_csv(g2_clean)

g2_time = time.time()
print("G2 is finished --- %s seconds ---" % (g2_time - g1_time))

print("All finished in %s seconds." % (time.time() - start_time))
