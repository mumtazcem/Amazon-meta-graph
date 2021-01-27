import pandas as pd

g1_file = "saved_dataframes/g1Db.csv"
g2_file = "saved_dataframes/g2Db.csv"
g1_clean = "saved_dataframes/g1Db_clean.csv"
g2_clean = "saved_dataframes/g2Db_clean.csv"

g1 = pd.read_csv(g1_file)
g2 = pd.read_csv(g2_file)

n1, col1 = g1.shape
n2, col2 = g2.shape

run_G1 = False
run_G2 = True

if run_G1:
    print("Running G1")
    for index, row in g1.iterrows():
        removeS = []
        for i in range(row['totalSimilar'] ):
            # similarity_indices: s1, s2, s3, s4 ,s5
            similarity_index = "s" + str(i + 1)
            similar_product_asin = row[similarity_index]
            # if the similar cell is null
            if isinstance(row[similarity_index], float):
                print("float")
                continue
            similar_product_row = g1[g1['ASIN'].str.contains(similar_product_asin)]
            if similar_product_row['ASIN'].empty :
                removeS.append(similarity_index);
                
        g1.at[index, 'totalSimilar'] = row['totalSimilar'] - len(removeS)
        for s in (removeS):
            g1.at[index, s] = None
        with open(g1_clean, 'w', newline='') as myfile:
            g1.to_csv(g1_clean)

            
if run_G2:
    print("Running G2")
    for index, row in g2.iterrows():
        removeS = []
        for i in range(row['totalSimilar'] ):
            # similarity_indices: s1, s2, s3, s4 ,s5
            similarity_index = "s" + str(i + 1)
            similar_product_asin = row[similarity_index]
            # if the similar cell is null
            if isinstance(row[similarity_index], float):
                print("float")
                continue
            similar_product_row = g2[g2['ASIN'].str.contains(similar_product_asin)]
            if similar_product_row['ASIN'].empty :
                removeS.append(similarity_index);
                
        g2.at[index, 'totalSimilar'] = row['totalSimilar'] - len(removeS)
        for s in (removeS):
            g2.at[index, s] = None
               
    with open(g2_clean, 'w', newline='') as myfile:
            g2.to_csv(g2_clean)



