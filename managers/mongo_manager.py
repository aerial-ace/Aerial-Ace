import motor.motor_asyncio

from managers import cache_manager, init_manager
from managers.logging_manager import get_logger

logger = get_logger()


class MongoManager:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]

    async def add_data(self, collection_name: str, entry: dict) -> bool:
        """
        Add data to the database in the provided collection
        Return true if data entry was successfull; false overwise
        """

        try:
            await self.db[collection_name].insert_one(entry)

        except Exception as e:  # noqa: BLE001
            logger.error(f"Failed to add data to db \n\tcollection : {collection_name}\n\terror : {e}")
            return False

        return True

    async def get_all_data(self, collection_name: str, query: dict[str, str]) -> list | None:
        """
        Fetch all data from the provided collection and using the provided query
        Return a list of data items fetched from the db; None if error occurred
        """

        try:
            result_cursor = await self.db[collection_name].find(query).to_list(length=None)

            # if no entry in the particular collection is present, create an empty entry into that collection
            if len(result_cursor) <= 0:
                server_id = query.get("server_id")

                if server_id is not None:
                    if collection_name == "battles":
                        return [await init_manager.register_guild_for_battles(server_id)]
                    elif collection_name == "servers":
                        return [await init_manager.register_guild_without_bs(server_id)]
                    elif collection_name == "tags":
                        return [await init_manager.register_guild_for_tags(server_id)]
                    elif collection_name == "donations":
                        return [await init_manager.register_guild_for_donations(server_id)]
                else:
                    logger.error(f"No server of found from this query : {query}")
                    return []

            return result_cursor

        except Exception as e:  # noqa: BLE001
            logger.error(f"Execption triggered while trying to fetch data from db {e}")
            return None

    async def get_documents_length(self, col_name: str, query: dict) -> int:
        """
        Return the number of items in the cursor returned by running query on the provided collection
        """

        count = await self.db[col_name].count_documents(query)
        return count

    async def remove_all_data(self, col_name: str, query: dict) -> bool:
        """
        Remove all data represented by the query in the provided collection
        Return true if successfull, false otherwise
        """

        try:
            await self.db[col_name].delete_many(query)
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error occurred while trying to delete many items from a collection\n\terror: {e}")
            return False

        return True

    async def update_all_data(self, col_name: str, query: dict, updated_data: dict) -> bool:
        """
        Update many items in the provided collection by running the provided query
        Return true if successfull, false otherwise
        """

        try:
            await self.db[col_name].update_many(query, {"$set": updated_data})

        except Exception as e:  # noqa: BLE001
            logger.error(f"Error while trying to update many in collection : {col_name}\n\terror : {e}")
            return False

        return True

    async def remove_entry(self, collection_name: str, query: dict, unset_data: dict) -> bool:
        """
        Remove one item from the collection using the provided query
        Return True if successfull, false otherwise
        """

        try:
            await self.db[collection_name].update_one(query, {"$unset": unset_data})
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error while trying to remove one in collection : {collection_name}\n\terror : {e}")
            return False

        return True

    async def update_spawnrate(self, server_id: str, active: bool | None, channel_id: str | None) -> bool:
        """
        Update the spawnrate data on the db as well as the cache manager
        Return true if successfull, false otherwise
        """

        updated_data = await cache_manager.update_spawnrates(server_id, active, channel_id)

        # Return if there is nothing to update.
        if updated_data is None:
            return True

        query = {"server_id": server_id}

        try:
            await self.db["spawnrate"].update_one(query, {"$set": updated_data}, upsert=True)

        except Exception as e:  # noqa: BLE001
            logger.error(f"Error while trying to update spawnrate data on db! \n\terror : {e}")
            return False

        return True

    async def update_shiny_counter(self, server_id, active, channel_id) -> bool:
        """
        Update the shinycount data on the db as well as the cache manager
        Return true if successfull, false otherwise
        """

        updated_data = await cache_manager.update_shinycounter(server_id, active, channel_id)

        # nothing to udpate
        if updated_data is None:
            return True

        query = {"server_id": str(server_id)}

        try:
            await self.db["shinycounter"].update_one(query, {"$set": updated_data}, upsert=True)

        except Exception as e:  # noqa: BLE001
            logger.error(f"Error while trying to update shinycounter data on db! \n\terror : {e}")
            return False

        return True

    async def increment_shiny_counter(self, server_id) -> bool:
        """
        Increment the shiny count on both db as well as the cache manager
        Return true if successfull, false otherwise
        """

        query = {"server_id": str(server_id)}

        # update the cache manager; return false if not updated
        if not await cache_manager.increment_shiny_counter(server_id):
            return False

        try:
            await self.db["shinycounter"].update_one(query, {"$inc": {"count": 1}})

        except Exception as e:  # noqa: BLE001
            logger.error(f"Error while trying to increment shinycounter data on db! \n\terror : {e}")
            return False

        return True


manager = None


def init_mongo(mongo_uri: str, database_name: str):
    global manager

    try:
        manager = MongoManager(mongo_uri, database_name)
    except Exception:
        logger.exception("Error while loading database")
        return False

    logger.info("Mongo Manager Loaded!")

    return True
