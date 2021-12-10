from pymongo import MongoClient, results
from pymongo import cursor

from data_uploader import MongoManager

class MongoManager:

    def __init__(self, mongo_uri : str, db_name : str) :
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]

    def add_data(self, collection_name : str, entry : dict) -> bool:

        try:
            self.db[collection_name].insert_one(entry)
        except:
            return False

        return True

    def get_all_data(self, collection_name : str, query : dict) -> cursor:

        try:
            result_cursor = self.db[collection_name].find(query)
        except:
            return None

        return result_cursor

    def get_documents_length(self, col_name : str, query : dict) -> int:
        count = self.db[col_name].count_documents(query)
        return count

    def remove_all_data(self, col_name : str, query : dict) -> bool:
        try:
            self.db[col_name].delete_many(query)
        except:
            return False

        return True

    def update_all_data(self, col_name : str, query : dict, updated_data: dict):
        self.db[col_name].update_many(query, {"$set" : updated_data})


manager = None

async def init_mongo(mongo_uri : str, database_name : str):
    global manager

    try:
        manager = MongoManager(mongo_uri, database_name)
    except Exception as e:
        print(f"Error while loading database {e}")
        return False

    return True