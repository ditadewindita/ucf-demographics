import pandas as pd
import numpy as np
# import json

from pymongo import MongoClient
from bson.objectid import ObjectId
# from bson import objectid

# JSON data keys
genders = ["Men", "Women"]
ethnicities = ["Asian", "Black/African American", "American Indian/Alaska Native", "Multi-racial", "Non-resident Alien", "Native Hawaiian/Other Pacific Islander", "White", "Not Specified", "Total"]
curr_term = "Fall 2016"

# DB connection info
url = "mongodb://ditadewindita:deetdeetadmin@ucfdemographics-shard-00-00-tyo4r.mongodb.net:27017,ucfdemographics-shard-00-01-tyo4r.mongodb.net:27017,ucfdemographics-shard-00-02-tyo4r.mongodb.net:27017/?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=UCFDemographics-shard-0&authSource=admin"
db_name = "ucf_demographics"
collection_name = "data_visualization_databycollege"

# Make DB connection
client = MongoClient(url)
db = client[db_name]
collection = db[collection_name]

# Read CSV
print("Reading CSV...")
df = pd.read_csv("fall2016.csv", header = [0, 1], sep = ',', error_bad_lines = False)

# collection.remove({})
# print("Cleared collection.")

# data_to_insert = []
for index, row in df.iterrows():
    print("Creating JSON for %s..." % row['College'][0])

    data_json = {}
    data_json['college'] = row['College'][0]
    data_json['college_code'] = row['College Code'][0]
    data_json['term'] = curr_term

    # Only insert if theres no existing entry for the same college and term
    if collection.find_one(data_json) != None:
        print("%s, %s data already exists. Skipping." % (row['College'][0], curr_term))
        continue

    ethnicity_data = []
    for e in ethnicities:
        ethnicity_data_json = {}
        ethnicity_data_json['ethnicity'] = e

        gender_data = {}
        for g in genders:
            gender_data[g.lower()] = row[e][g]

        ethnicity_data_json['total'] = gender_data

        if e == "Total":
            data_json['total'] = gender_data
        else:
            ethnicity_data.append(ethnicity_data_json)

    data_json['university_total'] = row['University Total'][0]
    data_json['data'] = ethnicity_data

    print("Inserting %s data into DB..." % row['College'][0])
    print("---> Created ObjectId: %s" % data_json['_id'])
    try:
        collection.insert_one(data_json)
    except:
        data_json['_id'] = ObjectId()
        print("---> Failed to insert %s data into DB" % row['College'][0])
    # data_to_insert.append(data_json)

    # print(data_json)

# collection.insert_many(data_to_insert)
