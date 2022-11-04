import csv
import json
import hashlib

# Storing the path to the input and output files
csvFilePath = "HNGi9 CSV FILE - Sheet1.csv"
jsonFilePath = "Sheet1.json"
outputCsvFilepath = "Sheet1.output.csv"

# A function to format or convert the attributes values to an object
def getAttriObj(attr):
    # Splitting attr (data type string) the argument by ";" into an array   
    splitted_attribute = attr.split(';')

    # This is the initial data of what will be returned in the function
    attributes = []

    # Looping through each element of the array
    for attribute in splitted_attribute:
        # Splitting each element by ":" into another array.
        each_attri = attribute.split(':')
        if each_attri[0] == '':
            continue

        # Adding the data that exists into the list of objects that will be returned.
        attributes.append({
            "trait_type": each_attri[0],
            "value": each_attri[len(each_attri) - 1]
        })

    return attributes


# A function to convert the attribues object to string
def getAttriList(attri):
    # This is the initial data of what will be returned in the function
    new_attr = []

    # Looping through each object of the array
    for ob in attri:
        new_attr.append(f'{ob["trait_type"]}:{ob["value"]}')

    # Converting the array to a string
    formated_attr = ";".join(new_attr)

    return formated_attr


obj_list = []

# Opening the csv file that is to be convertted to a json
with open(csvFilePath) as csvFile:
    # Reading the file
    csvReader = csv.DictReader(csvFile)

    csvReaderList = list(csvReader)
    total_length = len(csvReaderList)

    for rows in csvReaderList:
        # Creating an object for each row
        obj_list.append({
            'team names': rows['TEAM NAMES'],
            "format": "CHIP_0007",
            "name": rows['Filename'],
            "description": rows['Description'],
            "minting_tool": rows['Name'],
            "gender": rows['Gender'],
            "sensitive_content": False,
            "series_number": int(rows["Series Number"]),
            "series_total": total_length,
            "attributes": getAttriObj(rows['Attributes']),
            "uuid": rows['UUID'],
            "collection": {
                "name": "Zuri NFT Tickets for Free Lunch",
                "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
                "attributes": [
                    {
                        "type": "description",
                        "value": "Rewards for accomplishments during HNGi9."
                    }
                ]
            }
        })

# Looping through the object list and hashing each object
for i in range(len(obj_list)):
    readable_hash = hashlib.sha256(
        json.dumps(obj_list[i]).encode('utf8')).hexdigest()
    # Appending each hash to each object
    obj_list[i]['hash'] = readable_hash

    # Formatting each attributes from an object to a list
    obj_list[i]['attributes'] = getAttriList(obj_list[i]['attributes'])


# Writing the object from the csv into the json file
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(obj_list, indent=4))


# Converting the json file to a csv
with open(jsonFilePath) as json_file:
    jsondata = json.load(json_file)

# Opening the new output file
data_file = open(outputCsvFilepath, 'w', newline='')
csv_writer = csv.writer(data_file)

# The count is to ensures that we have our headers in a single rows
count = 0
valueList = []
for data in jsondata:
    if count == 0:
        headerList = list(data.keys())
        header = []
        valueList = header
        # This is to ensures that the output csv file columns is the same as that of the input
        for head in headerList:
            if head == 'format' or head == "minting_tool" or head == "sensitive_content" or head == "collection":
                continue
            header.append(head)

        # Writing the header from the formatted json file
        csv_writer.writerow(header)
        count += 1

    values = []

    # Appropritate data for each column
    for val in valueList:
        values.append(data[val])

    # Writing the data for each column
    csv_writer.writerow(values)

# Closing the output.csv file.
data_file.close()
