import discord
import os
import aerialace
import aerialace_data_manager

# Intents
intents = discord.Intents.all()
intents.typing = False
intents.reactions = True

# init
client = discord.Client(intents=intents)
server = None
server_id = None

admin_user_id = os.environ['ADMIN_ID']


# events
@client.event
async def on_guild_join(guild):

    await aerialace_data_manager.register_guild(client, guild)
    print("server was joined and registered")


@client.event
async def on_guild_remove(guild):

    await aerialace_data_manager.remove_guild(client, guild)
    print("server was removed")


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # get the server details
    global server, server_id
    if server == None:
        server = message.guild
        server_id = str(server.id)

    # get the message details
    msg = message.content.lower()
    member = message.author
    user_id = str(message.author.id)
    user_nick = member.display_name

    # help command
    if msg.startswith("-aa help"):
        help_embed = aerialace.get_help_embed(discord.Embed(),
                                              discord.Color.blue())
        await message.channel.send(embed=help_embed)

        return

    # say hello command
    if msg.startswith("-aa hello") or msg.startswith("-aa alola") or msg.startswith("-aa hola") or msg.startswith("-aa henlu") or msg.startswith("-aa hi"):
        await message.channel.send("> Alola **{name}**".format(name=user_nick))
        return

    # rolling command
    if msg.startswith("-aa roll"):

        max_roll = 100

        try:
            max_roll_str = aerialace.get_parameter(msg, "-aa roll")

            if max_roll_str == "":
                max_roll = 100
            elif int(max_roll_str) < 0:
                raise Exception()
            else:
                max_roll = int(max_roll_str)
        except:
            await message.channel.send(
                "Enter a valid upper index! Like this : ```-aa roll 100```")
            return

        roll = aerialace.roll(max_roll)

        await message.channel.send(
            "> **{name}** rolled and got {roll} :game_die:".format(
                name=user_nick, roll=roll))
        return

    # Random Pokemone command
    if (msg.startswith("-aa rp")) or msg.startswith("-aa rand_poke"):

        try:
            rand_poke = aerialace.get_random_poke()
        except Exception as excp:
            await message.channel.send(
                "> Some error occured while fetching random pokemon, the details have been send to the appropriate peeps"
            )
            print("--Error while fetching random pokemon : {e}".format(e=excp))
            return

        reply = aerialace.get_random_pokemon_embed(discord.Embed(), rand_poke,
                                                   discord.Color.blue(),
                                                   server_id, user_id)

        await message.channel.send(embed=reply)
        return

    # Dex search command
    if msg.startswith("-aa dex"):

        param = aerialace.get_parameter(msg, ["-aa dex"])
        pokeData = None

        try:
            pokeData = aerialace.get_poke_by_id(param)
        except Exception as excp:
            await message.channel.send(
                "> Mhan, that pokemon was not found in the pokedex, if you think this pokemon should be there in the dex, dm DevGa.me#0176"
            )
            print("--Error occured while showing a dex entry : {e}".format(
                e=excp))
            return

        reply = aerialace.get_dex_entry_embed(discord.Embed(), pokeData,
                                              discord.Color.blue())

        await message.channel.send(embed=reply)
        return

    # Register Favourite Pokemon command
    if msg.startswith("-aa set_fav") or msg.startswith("-aa sf"):
        param = aerialace.get_parameter(msg, ["-aa set_fav", "-aa sf"])

        reply = aerialace_data_manager.set_fav(server_id, user_id, param)
        await message.channel.send(reply)
        return

    # View favourite pokemon command
    if msg.startswith("-aa fav"):
        reply = aerialace_data_manager.get_fav(server_id, user_id)
        await message.channel.send(reply)
        return

    # get duelish stats command
    if msg.startswith("-aa stats"):
        param = aerialace.get_parameter(msg, "-aa stats")
        reply = aerialace_data_manager.get_stats_embed(
            discord.Embed(), param, discord.Color.blue())
        await message.channel.send(embed=reply)

        return

        # get duelish stats command
    if msg.startswith("-aa moveset") or msg.startswith("-aa ms"):
        poke = aerialace.get_parameter(msg, ["-aa ms", "-aa moveset"])
        reply = await aerialace_data_manager.get_moveset_embed(discord.Embed(), poke, discord.Color.blue())
        await message.channel.send(embed=reply)

        return

        # get tierlists command
    if msg.startswith("-aa tierlist") or msg.startswith("-aa tl"):
        param = aerialace.get_parameter(msg, ["tierlist", "-aa tl"])
        tl_link = aerialace_data_manager.get_tl(param)
        await message.channel.send(content="Source : P2HB \n {link}".format(
            link=tl_link))

        return

    # invite command
    if msg.startswith("-aa invite"):
        reply = aerialace.get_invite_embed(discord.Embed(),
                                           discord.Color.blue())
        await message.channel.send(embed=reply)

        return

    # register shiny commnad
    if msg.startswith("-aa tag"):
        tag = aerialace.get_parameter(msg, ["-aa tag"])
        reply = aerialace_data_manager.register_tag(server_id, user_id,
                                                    user_nick, tag)

        await message.channel.send(reply)

        return

    if msg.startswith("-aa tag_ping") or msg.startswith("-aa tp"):
        tag = aerialace.get_parameter(msg, ["-aa tp", "-aa tag_ping"])
        reply = aerialace_data_manager.get_tag_hunters(server_id, tag)

        await message.channel.send(reply)

        return

    # Admins Only
    # returns the json files of the data
    if msg.startswith("-aa fetch_data_files") or msg.startswith("-aa fdf"):
        if user_id == admin_user_id:
            await aerialace_data_manager.get_data_files(client)

        await message.channel.send("> Data files were sent to admins :}")

        return

    # command not found
    if msg.startswith("-aa "):
        await message.channel.send(
            "> -aa what? That command doesn't exist! \n> See all the available commands by using ```-aa help```")


token = os.environ['TOKEN']

client.run(token)
