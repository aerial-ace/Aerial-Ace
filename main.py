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
		
		try:
			rand_poke = aerialace.get_random_poke()
		except Exception as excp:
			await message.channel.send("> Some error occured while fetching random pokemon, the details have been send to the appropriate peeps")
			print("--Error while fetching random pokemon : {e}".format(e = excp))
			return

		reply = aerialace.get_random_pokemon_embed(discord.Embed(), rand_poke, discord.Color.blue())

		await message.channel.send(embed = reply)

	#search for pokemon using index
	if(msg.startswith("-aa dex")):

		param = aerialace.get_parameter(msg, "-aa dex")
		pokeData = None

		try:
			pokeData = aerialace.get_poke_by_id(param)
		except:
			await message.channel.send("> Mhan, that pokemon was not found in the pokedex, if you think this pokemon should be there in the dex, dm DevGa.me#0176")
			return

		reply = aerialace.get_dex_entry_embed(discord.Embed(), pokeData, discord.Color.blue())
		
		await message.channel.send(embed = reply)

	#rolling
	if msg.startswith("-aa roll"):
		max_roll = 100

		try:
			max_roll_str = aerialace.get_parameter(msg, "-aa roll")
			
			if max_roll_str == "":
				max_roll = 100
			else:
				max_roll = int(max_roll_str)
		except:
			await message.channel.send("Enter a valid upper index! Like this : ```-aa roll 100```")
			return

		roll = aerialace.roll(max_roll)

		await message.channel.send("> <@{user}> rolled {roll} :game_die:".format(user = user, roll = roll))
		
	#say hello
	if msg.startswith("-aa Hello") or msg.startswith("-aa Alola") or msg.startswith("-aa Hola") or msg.startswith("-aa Henlu") or msg.startswith("-aa Hi"):
		await message.channel.send("> Alola <@{user}>".format(user = user))

token = os.environ['TOKEN']

client.run(token)
