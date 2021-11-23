import discord
import json
import global_vars
import os


#return data files
async def get_data_files(client):
	stats_file = discord.File(global_vars.STATS_FILE_LOCATION)
	fav_file = discord.File(global_vars.FAV_FILE_LOCATION)
	server_file = discord.File(global_vars.SERVER_FILE_LOCATION)
	tag_file = discord.File(global_vars.TAG_FILE_LOCATION)

	data_files = [stats_file, fav_file, server_file, tag_file]

	#DM the files to the admins
	admin_id = int(os.environ['ADMIN_ID'])
	admin = client.get_user(admin_id)
	try:
		for file in data_files:
			await admin.send(file = file)
	except discord.Forbidden:
		print("Unable to send message to admins.")


#register server in data
async def register_guild(client, guild):
	
	server_id = str(guild.id)
	server_name = str(guild.name)

	#Load the data form the files
	fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
	fav_data = json.loads(fav_data_out.read())
	fav_data_out.close()

	server_data_out = open(global_vars.SERVER_FILE_LOCATION, "r")
	server_data = json.loads(server_data_out.read())
	server_data_out.close()

	tag_data_out = open(global_vars.TAG_FILE_LOCATION, "r")
	tag_data = json.loads(tag_data_out.read())
	tag_data_out.close()

	#update the data 
	if server_id not in list(fav_data.keys()):
		fav_data[str(server_id)] = {}

	if server_id not in list(tag_data.keys()):
		tag_data[str(server_id)] = {}

	server_data[server_id] = server_name

	#Save the changes to the files
	fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
	json_obj = json.dumps(fav_data)
	fav_data_in.write(json_obj)
	fav_data_in.close()

	server_data_in = open(global_vars.SERVER_FILE_LOCATION, "w")
	json_obj = json.dumps(server_data)
	server_data_in.write(json_obj)
	server_data_in.close()

	tag_data_in = open(global_vars.TAG_FILE_LOCATION, "w")
	json_obj = json.dumps(tag_data)
	tag_data_in.write(json_obj)
	tag_data_in.close()

	#Dm the admins on server joins
	admin_id = int(os.environ['ADMIN_ID'])
	admin = client.get_user(admin_id)
	try:
		await admin.send("Aerial Ace was added to **{server}** :]".format(server = guild.name))
	except discord.Forbidden:
		print("Unable to send message to admins. Btw, Aerial Ace was added to **{server}** :]".format(server = guild.name))

async def remove_guild(client, guild):

	server_id = str(guild.id)

	#Get the data from the files
	fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
	fav_data = json.loads(fav_data_out.read())
	fav_data_out.close()

	server_data_out = open(global_vars.SERVER_FILE_LOCATION, "r")
	server_data = json.loads(server_data_out.read())
	server_data_out.close()

	tag_data_out = open(global_vars.TAG_FILE_LOCATION, "r")
	tag_data = json.loads(tag_data_out.read())
	tag_data_out.close()

	#update the data 
	if server_id in list(fav_data.keys()):
		del fav_data[server_id]

	if server_id in list(tag_data.keys()):
		del tag_data[server_id]

	if server_id in (server_data.keys()):
		del server_data[server_id]

	#Save the data to the files
	fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
	json_obj = json.dumps(fav_data)
	fav_data_in.write(json_obj)
	fav_data_in.close()

	server_data_in = open(global_vars.SERVER_FILE_LOCATION, "w")
	json_obj = json.dumps(server_data)
	server_data_in.write(json_obj)
	server_data_in.close()

	tag_data_in = open(global_vars.TAG_FILE_LOCATION, "w")
	json_obj = json.dumps(tag_data)
	tag_data_in.write(json_obj)
	tag_data_in.close()

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

#get movesets
async def get_moveset_embed(embd, poke, color):
	moveset_file = open(global_vars.MOVESET_FILE_LOCATION, "r")
	moveset_data = json.loads(moveset_file.read())
	moveset_file.close()

	pokemons = list(moveset_data.keys())
	embd.color = color

	if poke in pokemons:
		embd.title = "{poke}'s moveset".format(poke = poke.capitalize())
		embd.description = "{ms}".format(ms = moveset_data[poke])
		return embd
	else:
		embd.title = "That pokemon was not found in the database"
		embd.description = "> If the name is correct then"
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
def register_tag(server_id, user_id, user_nick, tag):

	if tag == "":
		return "> Give a valid tag name like ```-aa tag espurr```"

	#Load data from files
	tag_file_out = open("data/tags.json", "r")
	tag_data = json.loads(tag_file_out.read())
	tag_file_out.close()

	current_tag = ""
	value_index = -1

	tag_keys = list(tag_data[server_id].keys())			#all the tags
	tag_values = list(tag_data[server_id].values())		#all the users

	for i in range(0, len(tag_values)):
		if user_id in tag_values[i]:
			value_index = i
			break

	#If tag doesn't exist, create and assign the user to it
	if value_index == -1:
		tag_data[server_id][tag] = [] 
		tag_data[server_id][tag].append(user_id)

	#if tag exist, move the user to current tag to new tag
	else:
		current_tag = tag_keys[value_index]

		if current_tag == tag:
			return "> {user} is already assigned to `{tag}` tag".format(user = user_nick, tag = tag.capitalize())

		tag_data[server_id][current_tag].remove(user_id)
		
		if len(tag_data[server_id][current_tag]) <= 0:
			del tag_data[server_id][current_tag]

		if tag in tag_keys:
			tag_data[server_id][tag].append(user_id)
		else:
			tag_data[server_id][tag] = []
			tag_data[server_id][tag].append(user_id)

	#Save the data into the files
	tag_data_in = open(global_vars.TAG_FILE_LOCATION, "w")
	json_obj = json.dumps(tag_data)
	tag_data_in.write(json_obj)
	tag_data_in.close()	

	if value_index == -1:
		return "> {user} was assigned to `{tag}` tag".format(user = user_nick, tag = tag.capitalize())

	if current_tag == None:
		return "> {user} was assigned to `{tag}` tag".format(user = user_nick, tag = tag.capitalize())
	else : 
		return "> {user} was removed from `{prev}` and assigned to `{new}` tag".format(user = user_nick, prev = current_tag.capitalize(), new = tag.capitalize())

#Get shiny tags
def get_tag_hunters(server_id, tag):
	#Get data from the file
	tag_data_out = open(global_vars.TAG_FILE_LOCATION, "r")
	tag_data = json.loads(tag_data_out.read())
	tag_data_out.close()

	if tag not in list(tag_data[server_id].keys()):
		return "> That tag doesn't exist"

	hunters = tag_data[server_id][tag]
	hunter_pings = ""
	number_of_hunters = len(hunters)
	
	for i in range(0, number_of_hunters):
		hunter_pings = hunter_pings + "<@{user}>".format(user = str(hunters[i]))
		if i <= number_of_hunters - 2:
			hunter_pings += " | "

	return "> Pinging users assigned to `{tag}` tag \n {users}".format(tag = tag.capitalize(), users = hunter_pings)
