import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

class PokeData:

	p_valid = False
	p_log = ""

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

	try:
		data = json.loads(general_response.text)
		flavor_data = json.loads(flavor_response.text)
	except:
		poke.p_valid = False
		poke.p_log = "Pokemon not found, try \n```-aa dex 69```"
		return poke

	poke.p_valid = True
	poke.p_log = "Valid Pokemon"

	poke.id = id

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

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if(message.author == client.user):
		return

	msg = message.content
	user = message.author.id

	#Random Pokemon
	if(msg.startswith("-aa rp")) or msg.startswith("-aa rand_poke"):
		rand_poke = get_random_poke()
		if rand_poke.p_valid == False:
			await message.channel.send(rand_poke.p_log)
			return

		reply = discord.Embed()
		reply.color = discord.Color.blue()

		reply.title = "**{0} : {1}**".format(rand_poke.id, rand_poke.name)
		print(rand_poke.name)

		description = ""
		description += "{0}".format(rand_poke.p_info)
		description += "\n\n"
		description += "**Height** : {h}m | **Weight** : {w}kg".format(h = rand_poke.p_height, w = rand_poke.p_weight)
		reply.description = description

		reply.set_image(url = rand_poke.image_link)

		await message.channel.send(embed = reply)

	#search for pokemon using index
	if(msg.startswith("-aa dex ")):
		poke_id = msg.replace("-aa dex ", "")
		poke_id = poke_id.strip()
		poke_id = int(poke_id)

		pokeData = get_poke_by_id(poke_id)
		if pokeData.p_valid == False:
			await message.channel.send(pokeData.p_log)
			return

		reply = discord.Embed()
		reply.color = discord.Color.blue()

		reply.title = "**{0} : {1}**".format(pokeData.id, pokeData.name)

		description = ""
		description += "{0}".format(pokeData.p_info)
		description += "\n\n"
		description += "**Height** : {h}m | **Weight** : {w}kg".format(h = pokeData.p_height, w = pokeData.p_weight)

		reply.description = description
		reply.set_image(url = pokeData.image_link)

		await message.channel.send(embed = reply)

	#rolling
	if msg.startswith("-aa roll"):
		random_num = random.randint(0, 100)

		await message.channel.send("<@{user}> rolled {roll} :game_die:".format(user = user, roll = random_num))
		
	#say hello
	if msg.startswith("-aa Hello") or msg.startswith("-aa Alola") or msg.startswith("-aa Hola") or msg.startswith("-aa Henlu") or msg.startswith("-aa Hi"):
		await message.channel.send("Alola <@{user}>".format(user = user))

token = os.environ['TOKEN']

client.run(token)
