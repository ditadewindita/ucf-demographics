import pandas as pd
import numpy as np
import os.path
# import json

from pymongo import MongoClient
from bson.objectid import ObjectId
# from bson import objectid

# JSON data keys
genders = ["Men", "Women"]
ethnicities = ["Asian", "Black/African American", "American Indian/Alaska Native", "Multi-racial", "Non-resident Alien", "Native Hawaiian/Other Pacific Islander", "White", "Not Specified", "Total"]
terms = ["Spring", "Summer", "Fall"]
years = [2016, 2017, 2018]

# DB connection info
url = "mongodb://ditadewindita:deetdeetadmin@ucfdemographics-shard-00-00-tyo4r.mongodb.net:27017,ucfdemographics-shard-00-01-tyo4r.mongodb.net:27017,ucfdemographics-shard-00-02-tyo4r.mongodb.net:27017/?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=UCFDemographics-shard-0&authSource=admin"
db_name = "ucf_demographics"
collection_name = "data_visualization_databycollege"

# Make DB connection
client = MongoClient(url)
db = client[db_name]
collection = db[collection_name]

# collection.remove({})
# print("Cleared collection.")

for term in terms:
    for year in years:
        curr_term = "%s %s" % (term, str(year))
        curr_filename = "%s_%s.csv" % (term.lower(), year)

        if os.path.isfile(curr_filename):
            print("Reading %s CSV..." % curr_term)
        else:
            print("Cannot find CSV for %s" % curr_term)
            continue

        df = pd.read_csv(curr_filename, header = [0, 1], sep = ',', error_bad_lines = False)
        print(df)
        res = input("---> Does this data frame look okay? (y/n):")

        if res == "n":
            print("---> Skipping CSV for %s..." % curr_term)
            continue

        # data_to_insert = []
        for index, row in df.iterrows():
            print("---> Creating JSON for %s..." % row['College'][0])

            data_json = {}
            data_json['college'] = row['College'][0]
            data_json['college_code'] = row['College Code'][0]
            data_json['term'] = term

            # Only insert if theres no existing entry for the same college and term
            if collection.find_one(data_json) != None:
                print("---> %s, %s data already exists. Updating...\n" % (row['College'][0], curr_term))
                collection.remove(data_json)
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
            data_json['year'] = year

            print("---> Inserting %s data into DB..." % row['College'][0])

            try:
                collection.insert_one(data_json)
                print("---> Successfully inserted %s data into DB." % row['College'][0])
            except:
                data_json['_id'] = ObjectId()
                print("---> Failed to insert %s data into DB." % row['College'][0])

            print("\n")
