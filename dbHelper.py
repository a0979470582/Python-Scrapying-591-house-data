from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
database = client["591data"]

#table_house是存完整api的資料
#table_detail是存題目要求的schema
def getTable(tableName):
    return database[tableName]

def insetOneDetail(house_dict):
    table_detail = database['table_detail']
    table_detail.insert_one(house_dict)

def isRepeat(postid):
    table_detail = database['table_detail']
    return table_detail.find({'postid':postid}).count() > 0
    
def insertManyHouse(house_list):
    table_house = database['table_house']
    table_house.insert_many(house_list)

def loadAllHouse():
    table_house = database['table_house']
    return table_house.find({})

def deleteRepeatData():
    table_house = database['table_house']
    house_list = table_house.find({},{ "id": 1})#[{'_id': ObjectId('6079a227e10e065df24211c8'), 'id': 10705634},...]

    id_list = []
    pending_list = []
    for house in house_list:
        if house['id'] in id_list:
            pending_list.append(house)
        else:
            id_list.append(house['id'])

    print(len(id_list))
    print(len(pending_list))

    for house in pending_list:
        myquery = { "_id":  house['_id']}
        table_house.delete_one(myquery)