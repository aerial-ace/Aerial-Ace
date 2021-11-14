import random
import requests
import json
from textwrap import TextWrapper

class PokeData:

	p_id = 0
	p_name = ""
	p_type = ""
	p_region = ""
	p_weight = 0.0
	p_height = 0.0
	image_link = ""
	p_info = ""

	def __init__(self, name = "", id = 0):
		self.name = name
		self.id = id


#for getting a pokemon of desired index
def get_poke_by_id(id):

	poke = PokeData()

	general_response = requests.get("https://pokeapi.co/api/v2/pokemon/{0}".format(id))
	flavor_response = requests.get("https://pokeapi.co/api/v2/pokemon-species/{0}/".format(id))

	data = json.loads(general_response.text)
	flavor_data = json.loads(flavor_response.text)

	poke.id = data["id"]

	#get name
	poke.name = data["forms"][0]["name"].capitalize()

	#get height and weight
	poke.p_height = float(data["height"])
	poke.p_weight = float(data["weight"])

	#get info
	allInfos = flavor_data["flavor_text_entries"]
	poke.p_info = "*NULL*"

	for i in allInfos:
		if i["language"]["name"] == "en":
			poke.p_info = i["flavor_text"]
			break

	#get image_link
	rp_image_link = data["sprites"]["front_default"]
	poke.image_link = rp_image_link

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

	embd.title = "**{0} : {1}**".format(pokeData.id, pokeData.name)
	print(pokeData.name)

	description = wrap_text(40, pokeData.p_info)

	embd.description = description

	embd.set_image(url = pokeData.image_link)

	return embd

def get_dex_entry_embed(embd, pokeData, color):
	embd.color = color
	embd.title = "**{0} : {1}**".format(pokeData.id, pokeData.name)

	description = wrap_text(40, pokeData.p_info)
	description += "\n"
	description += "**Height** : {h}m | **Weight** : {w}kg".format(h = pokeData.p_height, w = pokeData.p_weight)

	embd.description = description
	embd.set_image(url = pokeData.image_link)

	return embd