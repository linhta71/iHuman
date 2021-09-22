import csv
import json

def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows["pairID"]
            if key not in data:
                data[key] = {"question": [], "response": []}
            data[key]["question"].append(rows["Statement.QUESTION"])
            data[key]["response"].append(rows["Statement.RESPONSE"])

    # Open a json writer, and use the json.dumps()
    # function to dump data

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
         
# Driver Code
 
# Decide the two file paths according to your
# computer system
csvFilePath = r'iHuman.csv'
jsonFilePath = r'ihuman.json'
 
# Call the make_json function
make_json(csvFilePath, jsonFilePath)