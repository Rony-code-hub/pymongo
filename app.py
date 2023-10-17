
import os
import pprint
from pymongo import MongoClient  #pip3 install pymongo[srv]
from dotenv import load_dotenv, find_dotenv #pip3 install python-dotenv
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://rony:{password}@cluster2.ht42g97.mongodb.net/"

client = MongoClient(connection_string)

dbs = client.list_database_names()
# my_dbs = client.Habit_tracker  --Access my database
# my_dbs = client["Habit_tracker"]  -- Another way to Access my database (Habit_tracker) as like dictonary key syntax.
# My database is Habit_tracker

my_dbs = client.Habit_tracker
collections = my_dbs.list_collection_names() #Access my collection names (habits) in my database.

def inserted_data():
    collection_input = my_dbs.habits  #client.Habit_tracker.habits
    text_document = {
        'name': 'Rony',
        'age': 29
    }

    inserted_id = collection_input.insert_one(text_document).inserted_id #Create unique ID
    print(inserted_id)
    
#inserted_data()


production = client.production  #If database name (production) is not found then automatically create the production name as database.
person_collection = production.person_collection  #If collection name (person_collection) is not found then automatically create the person_collection name as collection.

def create_document():
    first_names = ["Rony", "Farjana", "Hafsa", "Raihan"]
    last_names = ["PK", "Begum", "Miskat", "Ali"]
    ages = [29, 23, 3, 34]

    docs = [] #Efficient way to add multiple document in collection (method- 2)

    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first_name": first_name, "last_name": last_name, "age": age}

        #person_collection.insert_one(doc) #Single document added in the new collection (method- 1)

        docs.append(doc) #Efficient way to add multiple document in collection (method- 2)
    
    person_collection.insert_many(docs) #Efficient way to add multiple document in collection (method- 2)

#create_document()

# Reading Document  point1. During reading no need to put database name.

def fine_people():
    people = person_collection.find()
    #print(list(people))  Also get data in a list
    
    for i in people:
        pprint.pprint(i)  # Use for Nice formatted

#fine_people()

#Find Specific data from the collection

def find_hafsa():
    hafsa = person_collection.find_one({"first_name": "Hafsa"}) #write specific data name to access
    #hafsa = person_collection.find_one({"first_name": "Hafsa", "last_name": "Miskat"}) More specific way
    pprint.pprint(hafsa)

#find_hafsa()

#Count collection number

def count_collection_num():
    number = person_collection.count_documents(filter={})
    #number = person_collection.count_documents(filter={"first_name": "Hafsa"})
    #number = person_collection.find().count()  Also work

    print(number)

#count_collection_num()

# Find data by _id

def get_data_by_id(spam):
    from bson.objectid import ObjectId

    _id = ObjectId(spam)

    data = person_collection.find_one({"_id": _id})
    pprint.pprint(data)
    
#get_data_by_id("6520d426e0a6444164ecfcf1")

# Access data conditionally gte and lte

def get_age_range(min_age, max_age):
    quary = {"$and": [
        {"age": {"$gte": min_age}},
        {"age": {"$lte": max_age}}
    ]}

    people = person_collection.find(quary).sort("age")
    for i in people:
        pprint.pprint(i)

#get_age_range(20, 30)

#@Get specific data

def get_specific_data():
    column = {"_id": 0, "first_name": 1, "last_name": 1} #0 mean No, 1 mean Yes
    people = person_collection.find({}, column)
    for i in people:
        pprint.pprint(i)
#get_specific_data()

#Updating data

def update_data(spam):
    from bson.objectid import ObjectId
    _id = ObjectId(spam)

    all_update = {
        "$set": {"new_field": True}, # Add new key in collection, Can be add multiple key with separation by ,

        "$inc": {"age": 1}, # Increment by 1 29 + 1 = 30
        "$rename": {"first_name": "first", "last_name": "last"} #rename key
    }

    person_collection.update_one({"_id": _id}, all_update)

#update_data("6520d426e0a6444164ecfcf0")

#Deleting key

def deleting_key(spam):
    from bson.objectid import ObjectId
    _id = ObjectId(spam)

    person_collection.update_one({"_id": _id}, {"$unset": {"new_field": ""}})

# deleting_key("6520d426e0a6444164ecfcf0")

#Replace value
def replace_value(spam):
    from bson.objectid import ObjectId
    _id = ObjectId(spam)

    new_update = {"first_name": "First Name", "last_name": "Last Name", "age": 100}

    person_collection.replace_one({"_id": _id}, new_update)

replace_value("6520d426e0a6444164ecfcf3")

#Delet data from collection.

def deleting_data(spam):
    from bson.objectid import ObjectId
    _id = ObjectId(spam)

    person_collection.delete_one({"_id": _id})
    #person_collection.delete_many({"something"})  #Deleting many data. Please chatGPT
    #person_collection.delete_many({}) #Delete Evrythings

# deleting_data("6520d426e0a6444164ecfcf3")

address = {
    "street": "12500 weapon st.",
    "village": "Bhuipur",
    "Union": "Gobindapur",
    "Thana": "Dupchanchia",
    "Dist": "Bogra"
}


def add_address_embd(spam, address, addr):
    from bson.objectid import ObjectId
    _id = ObjectId(spam)

    person_collection.update_one({"_id": _id}, {"$addToSet": {"addresses": address}})

# add_address_embd("6520d426e0a6444164ecfcf2", address)

def add_address_relationship(spam, address):
    from bson.objectid import ObjectId
    _id = ObjectId(spam)

    address = address.copy()
    address["owner_id"] = spam  #Ex: Add owner_id in address

    address_collection = production.address
    address_collection.insert_one(address)

add_address_relationship("6520d426e0a6444164ecfcf1", address)