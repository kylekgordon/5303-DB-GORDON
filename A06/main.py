
from fastapi import FastAPI, Form, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from trial import RestaurantUtils
from typing import Optional, List
from bson import ObjectId
import json
import uvicorn

app = FastAPI()
# connect to mongodb
cnx = MongoClient("mongodb://localhost:27017/")
# use businessData
db = cnx["businessData"]
# choose collection
clx = db['restaurants']

utils = RestaurantUtils()


@app.get("/")
async def root():
    return {"message": "Welcome to Totally Kyle"}


@app.get('/restaurants/')
async def get_all(page_size: int = Form(...), page_num: int = Form(...)):
    '''
    : Form-Data: 
    #  @param -> page_size: Number of restaurants to be returned per page
    #  @param: -> page_num: Page number to return to results
    : @
    : 
    '''
    description = "Paginated results of all Restaurants in NYC"
    cursor = list(utils.get_all(page_size, page_num))
    return {
        "status": 1 if len(cursor) > 0 else 0,
        "description": description,
        "size": len(cursor),
        "response": {
            "data": cursor
        }
    }


@app.get(
    '/get_by_distance/',
    response_description="List of all restaurants within a given distance",
)
async def get_by_distance(distance: int = Form(...), coords: List[float] = Form(...),
                          category: Optional[str] = Form(None)):
    description = "List of all restaurants within a given distance"
    cursor = list(utils.get_by_distance(distance, coords, category))
    return {
        "status": 1 if len(cursor) > 0 else 0,
        "description": description,
        "size": len(cursor),
        "response": {
            "data": cursor
        }
    }


@app.get('/zipcode/', response_description="Get restaurants locted within a list of zipcodes")
async def get_by_zipcode(ziplist: List[str] = Form(...)):
    description = "Get restaurants locted within a list of zipcodes"

    cursor = utils.get_by_zip_code(ziplist)
    cursor = list(cursor)
    return {
        "status": "Success" if len(cursor) > 0 else "Failed",
        "description": description,
        "size": len(cursor),
        "response": cursor
    }


@app.get('/categories')
async def get_category():
    descriptions = "Returns a list of all categories of restaurants in NYC"
    cursor = utils.get_by_category()
    cursor = list(cursor)
    return {
        "status": "Success" if len(cursor) > 0 else "Failed",
        "description": descriptions,
        "size": len(cursor),
        "response": cursor
    }


@app.get('/cuisine')
async def get_cuisine(cuisine: str = Form(...)):
    cursor = list(utils.get_by_cuisine(cuisine))
    description = "List of restaurants of a given type"
    return {
        "status": "Success" if len(cursor) > 0 else "Failed",
        "description": description,
        "size": len(cursor),
        "response": cursor
    }

# @app.post("/world/")
# async def create_item(World:World):
#     sql = f"""
#     INSERT INTO `world` (`id`, `name`, `continent`, `area`, `population`, `gdp`, `capital`, `tld`, `flag`)
#     VALUES ('{World.id}', '{World.name}', '{World.continent}', '{World.area}', '{World.population}', '{World.gdp}', '{World.capital}','{World.tld}', '{World.flag}')
#     """
#     res = cnx.query(sql)
#     return res

# @app.post("/teach/")
# async def create_item(Teach:Teach):

#     # prints go to console for debugging
#     print(Teach.id)

#     # build query using "item" concatenating both lines using +=
#     sql =  f"INSERT INTO `teacher` (`id`,`dept`, `phone`,`mobile`) "
#     sql += f"VALUES ('{Teach.id}','{Teach.dept}','{Teach.phone}','{Teach.mobile}');"

#     # run the query
#     res = cnx.query(sql)

#     # result has a few entries when it comes back, success is true if everything worked
#     # otherwise oops

#     # if statement just as example
#     # if res['success']:
#     #     return res
#     # else:
#     #     return {'message':'oops'}

#     # result has info for a successful query or failed query
#     return res

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003,
                log_level="info", reload=True)
