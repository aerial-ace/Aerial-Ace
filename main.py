import discord
import os
import aerialace

client = discord.Client()

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
		rand_poke = aerialace.get_random_poke()
		if rand_poke.p_valid == False:
			await message.channel.send(rand_poke.p_log)
			return

		reply = discord.Embed()
		reply.color = discord.Color.blue()

		reply.title = "**{0} : {1}**".format(rand_poke.id, rand_poke.name)
		print(rand_poke.name)

		description = aerialace.wrap_text(40, rand_poke.p_info)

		reply.description = description

		reply.set_image(url = rand_poke.image_link)

		await message.channel.send(embed = reply)

	#search for pokemon using index
	if(msg.startswith("-aa dex ")):
		poke_id = msg.replace("-aa dex ", "")
		poke_id = poke_id.strip()
		poke_id = int(poke_id)

		pokeData = aerialace.get_poke_by_id(poke_id)
		if pokeData.p_valid == False:
			await message.channel.send(pokeData.p_log)
			return

		reply = discord.Embed()
		reply.color = discord.Color.blue()

		reply.title = "**{0} : {1}**".format(pokeData.id, pokeData.name)

		description = aerialace.wrap_text(40, pokeData.p_info)
		description += "\n"
		description += "**Height** : {h}m | **Weight** : {w}kg".format(h = pokeData.p_height, w = pokeData.p_weight)

		reply.description = description
		reply.set_image(url = pokeData.image_link)

		await message.channel.send(embed = reply)

	#rolling
	if msg.startswith("-aa roll"):

		max_roll = 100

		try:
			max_roll_str = msg.replace("-aa roll", "").strip()
			if max_roll_str == "":
				max_roll = 100
			else:
				max_roll = int(max_roll_str)
		except:
			await message.channel.send("Enter a valid upper index! Like this : ```-aa roll 100```")
			return

		roll = aerialace.roll(max_roll)

		await message.channel.send("<@{user}> rolled {roll} :game_die:".format(user = user, roll = roll))
		
	#say hello
	if msg.startswith("-aa Hello") or msg.startswith("-aa Alola") or msg.startswith("-aa Hola") or msg.startswith("-aa Henlu") or msg.startswith("-aa Hi"):
		await message.channel.send("Alola <@{user}>".format(user = user))

token = os.environ['TOKEN']

client.run(token)
