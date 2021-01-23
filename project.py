import pandas as pd
import numpy as np

# Read all lines of the meta data into content list.
file_name = "amazon_first_100_mod.txt"
with open(file_name, encoding='utf8') as f:
    content = f.readlines()
# Remove the beginning and trailing white spaces.
content = [x.strip() for x in content]

idList = []
asinList = []
groupList = []
salesRankList = []
similarityList = []
totalReviewList = []
avgRatingList = []

reviews = []

currentId = 0
numCategory = 0

similarityDict = {}         # disctionary that holds similar items as 
bookIdList = []

for line in content:
    parser_colon = line.split(':')
    parser_space = line.split()

    if parser_colon[0] == "Id":
        currentId = parser_colon[1].strip()
        idList.append(currentId)
        customer_dictionary = {}

    elif parser_colon[0] == "ASIN":
        currentAsin = parser_colon[1].strip()
        asinList.append(currentAsin)

    elif parser_colon[0] == "group":
        currentGroup = parser_colon[1].strip()
        groupList.append(currentGroup)
        if currentGroup == "Book":
            bookIdList.append(currentId)

    elif parser_colon[0] == "salesrank":
        salesRankList.append(parser_colon[1].strip())

    elif parser_colon[0] == "similar":
        similarityList.append(parser_colon[1].strip())
        
        similarityLine = parser_colon[1].strip().split(' ')
        similarityLine= list(filter(None, similarityLine))
        while len(similarityLine) != 6:
            similarityLine.append(None)         # add none if there are less then 5 similar items
        similarityDict[currentId] = similarityLine

    elif parser_colon[0] == "categories" or numCategory != 0:
        if numCategory == 0:
            numCategory = int(parser_colon[1].strip())
        else:
            numCategory = numCategory - 1
            continue
            
    elif parser_colon[0] == "reviews" and parser_colon[1].strip() == "total":
        numReview = parser_colon[2].split(' ')[1]
        avrgRate = parser_colon[4].strip()
        totalReviewList.append(numReview)
        avgRatingList.append(avrgRate)

    # Remove ID and ASIN if product is discontinued
    elif parser_colon[0] == "discontinued product":
        groupList.append(None)
        salesRankList.append(None)
        similarityList.append(None)
        similarityDict[currentId] = [None, None, None, None, None, None]
        totalReviewList.append(None)
        avgRatingList.append(None)
        
        continue
        # removing disconitnued product may lead to conflict because asin lis are indexed as id
        #idList.remove(currentId)
        #asinList.remove(currentAsin)

    elif len(parser_space) > 2:
        if parser_space[1] == "cutomer:":
            # TODO customer data is gathered yet it is not assigned to their corresponding product counterparts.
            customer_dictionary = {'customerId': parser_space[2], 'rating': parser_space[4], 'voting': parser_space[6],
                                   'helpful': parser_space[8]}
            
        else:
            customer_dictionary = {'customerId': None, 'rating': None, 'voting': None, 'helpful': None}
            
        reviews.append(customer_dictionary)
        
previouslines = ['Id', 'title', 'group', 'categories', 'totalreviews', 'avgrating']
# TODO add similar data as arrays
# TODO add reviews as dictionary (maybe?)
dataset = pd.DataFrame(
    {'Id': idList, 'ASIN': asinList, 'group': groupList, 'salesrank': salesRankList, 'similar': similarityList,
     'totalReview': totalReviewList, 'avgRatingList': avgRatingList})
#print(dataset)

similarityDataSet = pd.DataFrame(similarityDict)
#print(similarityDataSet)

#----------------- generate binary similarity graph -------------------#
numId = len(idList)
binSimMatrix = np.zeros((numId,numId), dtype=np.int)

for idIndex in (bookIdList):
    prId = int(idIndex)
    numSimilarProduct = similarityDataSet.iloc[0, prId]
    if numSimilarProduct == None:
        continue
    else:
        for simId in range (1, int(numSimilarProduct)):
            try:
                similarAsin = similarityDataSet.iloc[simId, prId]
            except ValueError:
                continue
            try:
               similarId = asinList.index(similarAsin)
            except ValueError:
                continue
            binSimMatrix[prId,similarId] = 1

np.savetxt("binSimGraph.txt", binSimMatrix, fmt="%d")


# TODO construct graph2 using this data frame, there should be excessive searching through it!
