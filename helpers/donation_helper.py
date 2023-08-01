from managers import mongo_manager

from helpers import logger

async def set_channel(server_id:int, channel_id:int):

    query = {"server_id" : str(server_id)}

    try:
        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query=query,
            updated_data={
                "channel_id" : str(channel_id)
            }
        )

    except Exception as e:
        logger.Logger.logError(e, "Error Occurred while trying to change the donation channel")
        return False
    
    else:
        return True