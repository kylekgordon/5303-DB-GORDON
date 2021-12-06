import pymongo
import pprint
import random
#from bson.son import SON
#from bson import json_util, ObjectID #

# connect to mongodb
cnx = pymongo.MongoClient("mongodb://localhost:27017/")
# use businessData
db = cnx["businessData"]
# choose collection
coll = db['restaurants']


def listAllCollections(dbName=None):
    """
    Description:
        lists all collections in a db (just as an example)
    Params:
        dbName (string) : name of database to view collections (optional)
    Returns:
        list
    """
    if dbName:
        collections = cnx[dbName].list_collection_names()
    else:
        collections = db.list_collection_names()

    return collections


def findAllRestaurants():
    """
    Description: 
        Find all restaurants in collection
    Params:
        None
    Returns: 
        dict : {"result":list,"size":int}
    """

    res = list(coll.find())

    return {"result": res, "count": len(res)}


def findCuisineCounts():
    """
    Description: 
        Count all restaurants that serve a specific cuisine
    Params:
        None
    Returns: 
        list of cuisine counts
    """

    results = db['restaurants'].aggregate([

        # Group the documents and "count" via $sum on the values
        {"$group":
            {
                "_id": '$cuisine',
                "count": {"$sum": 1}
            }
         }
    ])

    return list(results)


def findRestaurantsByCuisine(cuisine=None):
    """
    Description: 
        Find all restaurants that serve a specific cuisine
    Params:
        cuisine (string) : type of restaurant to find
    Returns: 
        list
    """

    if cuisine == None:
        res = findCuisineCounts()
        cuisine = random.choice(res)['_id']

    res = coll.find({'cuisine': cuisine})

    return list(res)

# Restaurants
# Find all restaurants (paginated result)
# Find unique restaurant categories
# Find all restaurants in a category
# Find all restaurants in a list of 1 or more zip codes
# Find all restaurants near Point(x,y)
# Find all restaurants with a min rating of X


if __name__ == '__main__':
    print("\n", "="*80, "\n", "="*80)
    print("\nList all collections in 'businessData':\n")
    res = listAllCollections(dbName='businessData')
    print(res)

    print("\n", "="*80, "\n", "="*80)
    print("\nList counts of all restaurants:\n")
    res = findAllRestaurants()
    print(res["count"])

    print("\n", "="*80, "\n", "="*80)
    print("\nList counts of all unique cuisines:\n")
    res = findCuisineCounts()
    pprint.pprint(res)

    print("\n", "="*80, "\n", "="*80)
    print("\nList 5 restaurants by cuisine (no param = random cuisine):\n")
    res = findRestaurantsByCuisine()
    pprint.pprint(res[:5])
