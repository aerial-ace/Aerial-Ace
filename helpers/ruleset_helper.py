from discord import Embed
import random

from managers import mongo_manager
from helpers import logger
from config import NORMAL_COLOR

async def get_random_ruleset_embed() -> Embed:

    cursor = await mongo_manager.manager.get_all_data("rulesets", {})
    number_of_rules = await mongo_manager.manager.get_documents_length("rulesets", {})

    random_value = random.randint(0, number_of_rules - 1)
    random_ruleset = cursor[random_value]

    embd = Embed(title="#{} - {}".format(random_ruleset.get("id", random_value), random_ruleset.get("name", "Random Rule")), color=NORMAL_COLOR)
    embd.description = ""

    for i, j in enumerate(random_ruleset.get("rules", [])):
        embd.description += "\n**Rule {} **: {}".format(i, j)

    embd.description += "\n\nUploaded By : **{}**".format(random_ruleset.get("user", "Admins"))

    embd.set_footer(text="Have an amazing idea for rulesets? Suggest it at the Support Server.")

    return embd

async def add_ruleset(name:str, rules:list, user:str):

    number_of_rulesets = await mongo_manager.manager.get_documents_length("rulesets", {})

    new_db_entry = {
        "id" : number_of_rulesets + 1,
        "name" : name, 
        "rules" : rules,
        "user" : user
    }

    try:
        await mongo_manager.manager.add_data("rulesets", new_db_entry)
    except Exception as e:
        logger.Logger.logError(e, "Error occurred while adding ruleset to the db.")
    else:
        return "Entry Added! Id : {}".format(number_of_rulesets + 1)




    



