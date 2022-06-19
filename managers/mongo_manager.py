# from pymongo import MongoClient
# from pymongo import cursor
import motor.motor_asyncio

class MongoManager:

    def __init__(self, mongo_uri : str, db_name : str) :
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]

    async def add_data(self, collection_name : str, entry : dict) -> bool:

        try:
            await self.db[collection_name].insert_one(entry)
        except:
            return False

        return True

    async def get_all_data(self, collection_name : str, query : dict):

        try:
            result_cursor = await self.db[collection_name].find(query).to_list(length=100)
        except:
            return None

        return result_cursor

    async def get_documents_length(self, col_name : str, query : dict) -> int:
        count = await self.db[col_name].count_documents(query)
        return count

    async def remove_all_data(self, col_name : str, query : dict) -> bool:
        try:
            await self.db[col_name].delete_many(query)
        except:
            return False

        return True

    async def update_all_data(self, col_name : str, query : dict, updated_data: dict):
        await self.db[col_name].update_many(query, {"$set" : updated_data})


manager = None

def init_mongo(mongo_uri : str, database_name : str):
    global manager

    try:
        manager = MongoManager(mongo_uri, database_name)
    except Exception as e:
        print(f"Error while loading database {e}")
        return False

    return True