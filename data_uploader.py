from warnings import resetwarnings
import pymongo
from pymongo import MongoClient
import json

from pymongo import collection
from pymongo import mongo_client

class MongoManager:
    def __init__(self, db_name : str) -> None:
        self.client = MongoClient("***REMOVED***")
        self.db = self.client[f"{db_name}"]

    def add_data(self, collection_name : str, entry : dict) -> bool:

        try:
            self.db[f"{collection_name}"].insert_one(entry)
        except:
            return False

        return True

    def get_data(self, collection_name : str) -> bool:
        data = self.db[f"{collection_name}"].find({})
        return data

def get_data_from_file(filename:str) -> dict:
    file_location = f"data/{filename}.json"
    file_out = open(file_location, "r")
    file_data = json.loads(file_out.read())
    file_out.close()

    return file_data

def main():
    db_manager = MongoManager("aerialace")

    data = get_data_from_file("battle_log")

    items = list(data.keys())

    for i in items:
        server_id = i
        logs = data[i]

        entry = {
            "server_id" : server_id,
            "logs" : logs
        }

        db_manager.add_data("battles", entry)


if __name__ == "__main__":
    main()