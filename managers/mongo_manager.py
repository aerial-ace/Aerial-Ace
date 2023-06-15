import motor.motor_asyncio

from managers import init_manager
from helpers import logger

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

            # if no entry in the particular collection is present, create an empty entry into that collection
            if len(result_cursor) <= 0:
                if collection_name == "battles":
                    return [await init_manager.register_guild_for_battles(query.get("server_id"))]
                elif collection_name == "servers":
                    return [await init_manager.register_guild_without_bs(query.get("server_id"))]
                elif collection_name == "tags":
                    return [await init_manager.register_guild_for_tags(query.get("server_id"))]
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
        logger.Logger.logError(e, f"Error while loading database")
        return False

    return True