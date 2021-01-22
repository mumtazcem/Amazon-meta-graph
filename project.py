import pandas as pd
import numpy as np

# Read all lines of the meta data into content list.
file_name = "amazon_first_100.txt"
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
        groupList.append(parser_colon[1].strip())

    elif parser_colon[0] == "salesrank":
        salesRankList.append(parser_colon[1].strip())

    elif parser_colon[0] == "similar":
        # TODO similarities should be a dictionary so that instead of putting full line to the data frame,
        #  these should be added as array to the data frame.
        similarityList.append(parser_colon[1].strip())

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
        idList.remove(currentId)
        asinList.remove(currentAsin)

    elif len(parser_space) > 2:
        if parser_space[1] == "cutomer:":
            # TODO customer data is gathered yet it is not assigned to their corresponding product counterparts.
            customer_dictionary = {'customerId': parser_space[2], 'rating': parser_space[4], 'voting': parser_space[6],
                                   'helpful': parser_space[8]}
            reviews.append(customer_dictionary)

previouslines = ['Id', 'title', 'group', 'categories', 'totalreviews', 'avgrating']
# TODO add similar data as arrays
# TODO add reviews as dictionary (maybe?)
dataset = pd.DataFrame(
    {'Id': idList, 'ASIN': asinList, 'group': groupList, 'salesrank': salesRankList, 'similar': similarityList,
     'totalReview': totalReviewList, 'avgRatingList': avgRatingList})
print(dataset)

# TODO construct graph2 using this data frame, there should be excessive searching through it!
