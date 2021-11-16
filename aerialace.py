import random
import requests
import json
from textwrap import TextWrapper

class PokeData:

	p_id = 0
	p_name = ""
	p_types = ""
	p_region = ""
	p_weight = 0.0
	p_height = 0.0
	image_link = ""
	p_info = ""
	p_stats = {}


#for getting a pokemon of desired index
def get_poke_by_id(id):

	poke = PokeData()

	general_response = requests.get("https://pokeapi.co/api/v2/pokemon/{0}".format(id))
	data = json.loads(general_response.text)

	species_response = requests.get("https://pokeapi.co/api/v2/pokemon-species/{0}/".format(id))
	species_data = json.loads(species_response.text)

	generation_response = requests.get("https://pokeapi.co/api/v2/generation/{name}/".format(name = species_data["generation"]["name"]))
	generation_data = json.loads(generation_response.text)

	poke.p_id = data["id"]

	#get name
	poke.p_name = data["name"].capitalize()

	#get height and weight
	poke.p_height = float(data["height"])
	poke.p_weight = float(data["weight"])

	#get types
	types = data["types"]
	
	for i in range(0, len(types)):
		poke.p_types += types[i]["type"]["name"].capitalize()

		if i != len(types) - 1:
			poke.p_types += ' | '

	#get_region
	poke.p_region = generation_data["main_region"]["name"].capitalize()

	#get info
	allInfos = species_data["flavor_text_entries"]
	poke.p_info = "*NULL*"

	for i in allInfos:
		if i["language"]["name"] == "en":
			poke.p_info = i["flavor_text"]
			break

	#get image_link
	poke.image_link = data["sprites"]["front_default"] 

	#get stats
	stats = data["stats"]

	for i in range(0, len(stats)):
		stat_name = stats[i]["stat"]["name"]
		stat_value = stats[i]["base_stat"]
		poke.p_stats[stat_name] = stat_value

	return poke

#for getting a random pokemon 
def get_random_poke():

	rand_pokemon_id = random.randint(1, 898)
	
	poke = get_poke_by_id(rand_pokemon_id)

	return poke

#for wraping text
def wrap_text(width, text):
	wrapped_text = ""
	wrapper = TextWrapper(width)
	text_lines = wrapper.wrap(text)
	for line in text_lines:
		wrapped_text += "{line}\n".format(line = line)

	return wrapped_text

#rolling
def roll(max):
	roll = random.randint(0, max)
	return roll

def get_parameter(msg, removable_command):
	return msg.replace(removable_command, "").strip()

def get_random_pokemon_embed(embd, pokeData, color):

	embd.color = color

	embd.title = "**{0} : {1}**".format(pokeData.p_id, pokeData.p_name)
	print(pokeData.p_name)

	description = wrap_text(40, pokeData.p_info)

	embd.description = description

	embd.set_image(url = pokeData.image_link)

	return embd

def get_dex_entry_embed(embd, pokeData, color):
	embd.color = color
	embd.title = "**{0} : {1}**".format(pokeData.p_id, pokeData.p_name)

	description = wrap_text(40, pokeData.p_info)
	description += "\n"

	embd.add_field(name = "Height", value = "{h} m".format(h = pokeData.p_height), inline = True)
	embd.add_field(name = "Weight", value = "{w} kg".format(w = pokeData.p_weight), inline = True)
	embd.add_field(name = "Region", value = "{r}".format(r = pokeData.p_region), inline = True)
	embd.add_field(name = "Type(s)", value = "{t}".format(t = pokeData.p_types), inline = True)

	stats_string = """**HP** : {hp} \u2800 | **ATK** : {atk} | **DEF** : {df}
					  **SPAT** : {spat} | **SPDF** : {spdf} | **SPD** : {spd}""".format(hp = pokeData.p_stats["hp"], atk = pokeData.p_stats["attack"], df = pokeData.p_stats["defense"], spat = pokeData.p_stats["special-attack"], spdf = pokeData.p_stats["special-defense"], spd = pokeData.p_stats["speed"])
	embd.add_field(name = "Stats", value = stats_string, inline = False)

	embd.description = description
	embd.set_image(url = pokeData.image_link)

	return embd

#Set the favourite pokemon of the user
def set_fav(server_id, user_id, poke_name):
	
	#get the data from the file
	fav_data_out = open("data/fav_data.json", "r")
	fav_data = json.loads(fav_data_out.read())
	fav_data_out.close()

	#update the data 
	fav_data[server_id][user_id] = poke_name

	#save the data
	fav_data_in = open("data/fav_data.json", "w")
	json_obj = json.dumps(fav_data)
	fav_data_in.write(json_obj)
	fav_data_in.close()

	return "> Your favourite pokemon is now **{fav}**. Check it using ```-aa fav```".format(fav = poke_name)
	

#Get the favourite pokemon of the user
def get_fav(server_id, user_id):

	fav_data_raw = open("data/fav_data.json", "r").read() 	# string data from the json file
	fav_data = json.loads(fav_data_raw)					  	# dictionary data from the json file

	server_list = list(fav_data.keys())						# all the registered servers

	if server_id in server_list:
		users = list(fav_data[server_id].keys())
		if user_id in users:
			fav_poke = fav_data[server_id][user_id]
			return "> Your favourite pokemon is **{}**".format(fav_poke)
		else:
			return "> User was not found in the database, set you favourite using ```-aa set_fav <pokemon>```"
	else:
		return "> Server was not found!"
