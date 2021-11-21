import discord
import json
import global_vars
import os


#return data files
def get_data_files():
	stats_file = discord.File(global_vars.STATS_FILE_LOCATION)
	fav_file = discord.File(global_vars.FAV_FILE_LOCATION)

	return {"stats" : stats_file, "fav" : fav_file}

#register server in data
async def register_guild(client, guild):
	
	server_id = str(guild.id)
	server_name = str(guild.name)

	#get the data from the file
	fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
	fav_data = json.loads(fav_data_out.read())
	fav_data_out.close()

	server_data_out = open(global_vars.SERVER_FILE_LOCATION, "r")
	server_data = json.loads(server_data_out.read())
	server_data_out.close()

	#update the data 
	if server_id not in list(fav_data.keys()):
		fav_data[str(server_id)] = {}

	server_data[server_id] = server_name

	#save the data
	fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
	json_obj = json.dumps(fav_data)
	fav_data_in.write(json_obj)
	fav_data_in.close()

	server_data_in = open(global_vars.SERVER_FILE_LOCATION, "w")
	json_obj = json.dumps(server_data)
	server_data_in.write(json_obj)
	server_data_in.close()

	#Dm the admins on server joins
	admin_id = int(os.environ['ADMIN_ID'])
	admin = client.get_user(admin_id)
	try:
		await admin.send("Aerial Ace was added to **{server}** :]".format(server = guild.name))
	except discord.Forbidden:
		print("Unable to send message to admins. Btw, Aerial Ace was added to **{server}** :]".format(server = guild.name))

async def remove_guild(client, guild):

	server_id = str(guild.id)

	#get the data from the file
	fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
	fav_data = json.loads(fav_data_out.read())
	fav_data_out.close()

	server_data_out = open(global_vars.SERVER_FILE_LOCATION, "r")
	server_data = json.loads(server_data_out.read())
	server_data_out.close()

	#update the data 
	if server_id in list(fav_data.keys()):
		del fav_data[server_id]
	
	if server_id in (server_data.keys()):
		del server_data[server_id]

	#save the data
	fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
	json_obj = json.dumps(fav_data)
	fav_data_in.write(json_obj)
	fav_data_in.close()

	server_data_in = open(global_vars.SERVER_FILE_LOCATION, "w")
	json_obj = json.dumps(server_data)
	server_data_in.write(json_obj)
	server_data_in.close()

	#Dm the admins on server removal
	admin_id = int(os.environ['ADMIN_ID'])
	admin = client.get_user(admin_id)

	try:
		await admin.send("Aerial Ace was removed from **{server}** :_:".format(server = guild.name))
	except discord.Forbidden:
		print("Unable to send message to the admin. Btw, Aerial Ace was removed from {server} :_:".format(server = guild.name))


#Set the favourite pokemon of the user
def set_fav(server_id, user_id, poke_name):
	
	if poke_name == "":
		return "> Breh, give a pokemon name as a parameter like ```-aa set_fav espurr```"

	#get the data from the file
	fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
	fav_data = json.loads(fav_data_out.read())
	fav_data_out.close()

	#update the data 
	fav_data[server_id][user_id] = poke_name

	#save the data
	fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
	json_obj = json.dumps(fav_data)
	fav_data_in.write(json_obj)
	fav_data_in.close()

	return "> Your favourite pokemon is now **{fav}**. Check it using ```-aa fav```".format(fav = poke_name)
	

#Get the favourite pokemon of the user
def get_fav(server_id, user_id):

	fav_data_raw = open(global_vars.FAV_FILE_LOCATION, "r").read() 	# string data from the json file
	fav_data = json.loads(fav_data_raw)					  			# dictionary data from the json file

	server_list = list(fav_data.keys())								# all the registered servers

	if server_id in server_list:
		users = list(fav_data[server_id].keys())
		if user_id in users:
			fav_poke = fav_data[server_id][user_id]
			return "> Your favourite pokemon is **{}**".format(fav_poke.capitalize())
		else:
			return "> User was not found in the database, set you favourite using ```-aa set_fav <pokemon>```"
	else:
		return "> Server was not found!"

#get duelish statss
def get_stats_embed(embd, pokemon, color):
	stats_file = open(global_vars.STATS_FILE_LOCATION, "r")
	stats_data_raw = stats_file.read()
	stats_data = json.loads(stats_data_raw)

	pokemons = list(stats_data.keys())
	embd.color = color

	if pokemon in pokemons:
		embd.title = "{poke}'s Stats".format(poke = pokemon.capitalize())
		embd.description = "HP, Defense, Sp.Defense and Speed are `The more the better` stats \n"
		embd.add_field(name = "Stats", value = "> {stats}".format(stats = stats_data[pokemon]), inline = False)

		return embd

	else:
		embd.title = "That pokemon was not found in the database"
		embd.description = "> If the name is correct then \n"
		embd.description += "> PROBABLY this pokemon is not good for battling"
		return embd

#return tierlists
def get_tl(list_name):

	if list_name == "rare":
		return global_vars.RARE_TL
	elif list_name == "mega":
		return global_vars.MEGA_TL	
	elif list_name == "common":
		return global_vars.COMMON_TL
	elif list_name == "normal":
		return global_vars.NORMAL_TL	
	elif list_name == "fire":
		return global_vars.FIRE_TL
	elif list_name == "water":
		return global_vars.WATER_TL
	elif list_name == "grass":
		return global_vars.GRASS_TL
	elif list_name == "electric":
		return global_vars.ELECTRIC_TL
	elif list_name == "psychic":
		return global_vars.PSYCHIC_TL
	elif list_name == "rock":
		return global_vars.ROCK_TL
	elif list_name == "ground":
		return global_vars.GROUND_TL
	elif list_name == "fighting":
		return global_vars.FIGHTING_TL
	elif list_name == "ghost":
		return global_vars.GHOST_TL
	elif list_name == "dark":
		return global_vars.DARK_TL
	elif list_name == "ice":
		return global_vars.ICE_TL
	elif list_name == "fairy":
		return global_vars.FAIRY_TL
	elif list_name == "dragon":
		return global_vars.DRAGON_TL
	elif list_name == "steel":
		return global_vars.STEEL_TL
	else:
		return """> That tierlist was not found, these tierlists are availible
					```common | mega | ```"""

#register shiny tags
def register_tag(server_id, user_id, tag):
	tag_file_out = open("data/tags.json", "r")
	tag_data = json.loads(tag_file_out.read())

	current_tag = None
	tags = tag_data[server_id]	#dictionary of all the tags and thier users
	for i in (tags.values()):
		if user_id in i:
			current_tag = tags.index(i)

	print(current_tag)

	#remove the user from their current tag
	#add the user to the new tag
	
	
