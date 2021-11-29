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

admin_user_id = os.environ['ADMIN_ID']


@client.event
async def on_guild_join(guild_joined):
    await aerialace_data_manager.register_guild(client, guild_joined)
    print("server was joined and registered")


@client.event
async def on_guild_remove(guild_removed):
    await aerialace_data_manager.remove_guild(client, guild_removed)
    print("server was removed")


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user or message.content.lower().startswith("-aa") is False:
        return

    guild = message.guild
    server_id = str(guild.id)

    # get the message details
    msg = ((message.content.lower()).replace("-aa", "")).strip()
    member = message.author
    user_id = str(message.author.id)
    user_nick = member.display_name

    # help command
    if msg.startswith("help"):
        help_embed = aerialace.get_help_embed(discord.Embed(), discord.Color.blue())
        await message.channel.send(embed=help_embed)

        return

    # say hello command
    hello_commands = ["hello", "alola", "hola", "henlu", "helu", "hi", "sup"]
    if msg in hello_commands:
        await message.channel.send("> Alola **{name}**".format(name=user_nick))
        return

    # rolling command
    if msg.startswith("roll"):

        try:
            max_roll_str = aerialace.get_parameter(msg, ["roll"])

            if max_roll_str == "":
                max_roll = 100
            elif int(max_roll_str) < 0:
                raise ValueError()
            else:
                max_roll = int(max_roll_str)
        except TypeError or ValueError as e:
            await message.channel.send("Enter a valid upper index! Like this : ```-aa roll 100```")
            print(e)
            return

        roll = aerialace.roll(max_roll)

        await message.channel.send(
            "> **{name}** rolled and got {roll} :game_die:".format(name=user_nick, roll=roll))
        return

    # Random Pokemon command
    if (msg.startswith("rp")) or msg.startswith("rand_poke"):

        try:
            rand_poke = aerialace.get_random_poke()
        except Exception as e:
            await message.channel.send(
                "> Some error occurred while fetching random pokemon, errors were registered"
            )
            print("--Error while fetching random pokemon : {exception}".format(exception=e))
            return

        reply = aerialace.get_random_pokemon_embed(discord.Embed(), rand_poke, discord.Color.blue(), server_id, user_id)

        await message.channel.send(embed=reply)
        return

    # Dex search command
    if msg.startswith("dex ") or msg.startswith("d "):

        param = aerialace.get_parameter(msg, ["dex", "d"])

        try:
            poke_data = aerialace.get_poke_by_id(param)
        except Exception as e:
            await message.channel.send(
                "> Mhan, that pokemon was not found in the pokedex, if this is not desirable, dm DevGa.me#0176"
            )
            print("--Error occurred while showing a dex entry : {e}".format(e=e))
            return

        reply = aerialace.get_dex_entry_embed(discord.Embed(), poke_data, discord.Color.blue())

        await message.channel.send(embed=reply)
        return

    # Register Favourite Pokemon command
    if msg.startswith("set_fav ") or msg.startswith("sf "):
        param = aerialace.get_parameter(msg, ["set_fav", "sf"])

        reply = aerialace_data_manager.set_fav(server_id, user_id, param)
        await message.channel.send(reply)
        return

    # View favourite pokemon command
    if msg.startswith("fav"):
        reply = aerialace_data_manager.get_fav(server_id, user_id)
        await message.channel.send(reply)
        return

    # get duelish stats command
    if msg.startswith("stats "):
        param = aerialace.get_parameter(msg, ["stats"])
        reply = aerialace_data_manager.get_stats_embed(discord.Embed(), param, discord.Color.blue())
        await message.channel.send(embed=reply)

        return

    # get duelish stats command
    if msg.startswith("moveset ") or msg.startswith("ms "):
        poke = aerialace.get_parameter(msg, ["ms", "moveset"])
        reply = await aerialace_data_manager.get_moveset_embed(discord.Embed(), poke, discord.Color.blue())
        await message.channel.send(embed=reply)

        return

    # get tierlist command
    if msg.startswith("tierlist ") or msg.startswith("tl "):
        param = aerialace.get_parameter(msg, ["tierlist", "tl"])
        tl_link = aerialace_data_manager.get_tl(param)
        await message.channel.send(content="Source : P2HB \n {link}".format(link=tl_link))

        return

    # invite command
    if msg.startswith("invite"):
        reply = aerialace.get_invite_embed(discord.Embed(), discord.Color.blue())
        await message.channel.send(embed=reply)

        return

    # register shiny command
    if msg.startswith("tag "):
        tag = aerialace.get_parameter(msg, ["tag"])
        reply = aerialace_data_manager.register_tag(server_id, user_id, user_nick, tag)

        await message.channel.send(reply)

        return

    # ping user with tag command
    if msg.startswith("tag_ping ") or msg.startswith("tp "):
        tag = aerialace.get_parameter(msg, ["tp", "tag_ping"])
        reply = aerialace_data_manager.get_tag_hunters(server_id, tag)

        await message.channel.send(reply)

        return

    # logs the battle and update the leaderboard
    if msg.startswith("log_battle ") or msg.startswith("lb "):
        players = aerialace.get_winner_looser(msg)

        info = await aerialace.get_battle_acceptance(client, message, players[0], players[1])

        if info == "accepted":
            reply = aerialace_data_manager.register_battle_log(server_id, players[0], players[1])
        elif info == "notaccepted":
            reply = "> Battle Log was not accepted"
        else:
            return

        await message.channel.send(reply)

        return

    # Display the battle score of the user
    if msg.startswith("battle_score") or msg.startswith("bs"):

        score = aerialace_data_manager.get_battle_score(server_id, member)

        await message.channel.send(score)

        return

    if msg.startswith("battle_lb") or msg.startswith("blb"):
        reply = await aerialace_data_manager.get_battle_leaderboard_embed(client, guild)
        await message.channel.send(embed=reply)
        return

    # Admins Only
    # returns the json files of the data
    if msg.startswith("fetch_data_files") or msg.startswith("fdf"):
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
