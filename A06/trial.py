
from pymongo import MongoClient
from pprint import pprint
import json

class RestaurantUtils:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.businessData
        self.collection = self.db.updated_restaurant
    def convertToGeoJSON():
        '''
        : @param: None
        : description: 
        '''
        restaurantsList = []
        coords = []
        with open('restaurant.json') as file:
            for restaurant in file:
                restDict = json.loads(restaurant)
                coords = restDict["address"]["coord"]
                if coords:
                    restDict["location"] = {
                        "type" : "Point",
                        "coordinates" : coords,
                    }
                    del restDict["address"]["coord"]
                    restaurantsList.append(restDict)
        with open('restaurantData.json', 'w+') as new_file:
            for newRestaurant in restaurantsList:
                rest_obj = json.dump(newRestaurant, new_file)
    
    # Find all restaurants in a list
    def get_all(self,page_size, page_num):
        skips = page_size * (page_num -1)
        cursor = self.collection.find().skip(skips).limit(page_size)
        return list(cursor)
    # Find all restaurants in a list by cuisine
    def get_by_cuisine(self,restaurant_type):
        results = self.collection.find({"cuisine": restaurant_type})
        return list(results)

    # Find all restaurants in a list by category
    def get_by_category(self):
        cursor = self.collection.distinct("cuisine")
        return list(cursor)

    # Find all restaurants in a list of 1 or more zip codes
    def get_by_zip_code(self,zip_list):
        temp = self.collection.find(
            {'address.zipcode':
                {'$in': zip_list}})
        return list(temp)

    # Find all restaurants near Point(x,y)
    def get_by_distance(self, distance, coords, category=None):
        geo_object = {}
        geo_object = { "near": {"type": "Point","coordinates" : coords},
                    "distanceField" : "dist.calculated",
                    "maxDistance": distance,
                    "includeLocs" : "dist.location",
                    "spherical" : "true"
                    }
        if(category):
            geo_object["query"]= {"cuisine" : category}
        pprint(geo_object)
        cursor = self.collection.aggregate([{"$geoNear": geo_object}])
        return list(cursor)


if __name__ == '__main__':
    # #! ***********************************************************************#
    # Convert JSON to correct data fields for geojson
    #convertToGeoJSON()

    # client = MongoClient("mongodb://localhost:27017/")
    # db = client.NYC
    # collection = db.geo_restaurant
    utils = RestaurantUtils()
    # #! ***********************************************************************#
    # Collect paginated results
    # results = utils.find_all(10, 3)
    # pprint(len(results))

    # #! ***********************************************************************#
    # Find restaurants by cuisine
    # restaurant = "Bakery"
    # results = utils.find_by_cuisine(restaurant)
    # pprint(results)

    # #! ***********************************************************************#
    # Find unique categories of restaurant
    # results = utils.get_unique_categories()
    # pprint(results)

    # #! ***********************************************************************#
    # Find restaurants by zipcode 
    zip_list = []
    zip_list.append("11234")
    results = utils.get_by_zip_code(zip_list)
    pprint(results)

    # #! ***********************************************************************#
    # # get by distance
    # results = utils.get_by_distance( 1000,[-73.856077,40.848447],"Café/Coffee/Tea")
    # pprint(len(results))