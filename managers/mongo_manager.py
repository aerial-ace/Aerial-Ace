from motor import motor_asyncio
import logging

from managers import init_manager
from managers import cache_manager


class MongoManager:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]

    async def add_data(self, collection_name: str, entry: dict) -> bool:
        try:
            await self.db[collection_name].insert_one(entry)
        except Exception:
            return False

        return True

    async def get_all_data(self, collection_name: str, query: dict):
        try:
            result_cursor = await self.db[collection_name].find(query).to_list(length=None)

            # if no entry in the particular collection is present, create an empty entry into that collection
            if len(result_cursor) <= 0:
                if collection_name == "battles":
                    return [await init_manager.register_guild_for_battles(query.get("server_id"))]
                elif collection_name == "servers":
                    return [await init_manager.register_guild_without_bs(query.get("server_id"))]
                elif collection_name == "tags":
                    return [await init_manager.register_guild_for_tags(query.get("server_id"))]
                elif collection_name == "donations":
                    return [await init_manager.register_guild_for_donations(query.get("server_id"))]
        except Exception:
            return None

        return result_cursor

    async def get_documents_length(self, col_name: str, query: dict) -> int:
        count = await self.db[col_name].count_documents(query)
        return count

    async def remove_all_data(self, col_name: str, query: dict) -> bool:
        try:
            await self.db[col_name].delete_many(query)
        except Exception:
            return False

        return True

    async def update_all_data(self, col_name: str, query: dict, updated_data: dict):
        await self.db[col_name].update_many(query, {"$set": updated_data})

    async def remove_entry(self, collection_name: str, query: dict, unset_data: dict):
        await self.db[collection_name].update_one(query, {"$unset": unset_data})

    async def update_spawnrate(self, server_id: str, active: bool, channel_id: str):
        updated_data = await cache_manager.update_spawnrates(server_id, active, channel_id)

        # Return if there is nothing to update.
        if updated_data is None:
            return

        query = {"server_id": server_id}

        await self.db["spawnrate"].update_one(query, {"$set": updated_data}, upsert=True)

    async def update_shiny_counter(self, server_id, active, channel_id):
        updated_data = await cache_manager.update_shinycounter(server_id, active, channel_id)

        if updated_data is None:
            return

        query = {"server_id": str(server_id)}

        await self.db["shinycounter"].update_one(query, {"$set": updated_data}, upsert=True)

    async def increment_shiny_counter(self, server_id):
        query = {"server_id": str(server_id)}

        await cache_manager.increment_shiny_counter(server_id)

        await self.db["shinycounter"].update_one(query, {"$inc": {"count": 1}})


manager = None


def init_mongo(mongo_uri: str, database_name: str):
    global manager

    try:
        manager = MongoManager(mongo_uri, database_name)
    except Exception:
        logging.exception("Error while loading database")
        return False

    return True
