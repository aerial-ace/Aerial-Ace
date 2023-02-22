import discord
from discord.ext import commands
import random

from helpers import general_helper
import config

# returns a value for roll
async def roll(max_value, user) -> str:

    if max_value < 0:
        return f"> **{user.name}** rolled and got ||Nothing|| :]"

    random_value = random.randint(0, max_value)
    return f"> **{user.name}** rolled and got {random_value} :game_die: [0 - {max_value}]"

# returns the about the bot embed
async def get_about_embed(ctx) -> discord.Embed:
    embd = discord.Embed(title="__ABOUT - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = "Aerial Ace = Pokedex + Poketwo Helper Bot"

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Prefix",
        value="`-aa ` and `aa.`",
        inline=True
    )
    embd.add_field(
        name=f"{config.BULLET_EMOJI}Support Server",
        value=f"[Click here]({config.SUPPORT_SERVER_LINK})",
        inline=True
    )
    embd.add_field(
        name=f"{config.BULLET_EMOJI}Vote Link",
        value=f"[Click Here]({config.VOTE_LINK})",
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Servers",
        value=len(ctx.bot.guilds),
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Invite",
        value=f"[Click here]({config.INVITE_LINK})",
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Ping",
        value=str(round(ctx.bot.latency * 100, 2)),
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Language",
        value="Python 3.10",
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Library",
        value="[py-cord](https://github.com/Pycord-Development/pycord)",
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Repository",
        value=f"[Click here]({config.REPO_LINK})",
        inline=True
    )

    bot:commands.Bot = ctx.bot

    shards = bot.shard_count

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Shards",
        value="{}".format(shards),
        inline=True
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Source Details",
        value=f"**Aerial Ace** is an open source project released under GNU GPL v3 license.\nComplete source of the project is available on the github page (links above).\nRepo stars are appreciated :3",
        inline=False
    )

    embd.add_field(
        name=f"{config.BULLET_EMOJI}Made with  <3  by **Dev**",
        value=f"**Discord** : [DevGa.me]({config.DEVELOPER_DISCORD_PROFILE_LINK})\n**Github** : [Devanshu19]({config.GITHUB_PROFILE_LINK})",
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# returns the vote embed
async def get_vote_embed() -> discord.Embed:
    embd = discord.Embed(title="__Vote for Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"You can help Aerial Ace by voting for it.\n**Thank you** if you voted :3\n"
    embd.description += f"Vote Link : [Click here]({config.VOTE_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# returns the support server embed
async def get_support_server_embed() -> discord.Embed:
    embd = discord.Embed(title="__Support Server__", color=config.NORMAL_COLOR)
    embd.description = f"Join the support server for reporting bugs, suggesting features,\ngetting help...you got it.\n[Click here to join]({config.SUPPORT_SERVER_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# returns the invite embed
async def get_invite_embed() -> discord.Embed:
    embd = discord.Embed(title="__Invite - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = "Invite Aerial Ace to your server using this link : \n\n"
    embd.description += f"Link : [Click Here]({config.INVITE_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# logs the suggestions
async def register_suggestion(ctx, text : list()) -> None:

    suggestion_channel : discord.TextChannel = ctx.bot.get_guild(config.SUPPORT_SERVER_ID).get_channel(config.SUGGESTION_LOG_CHANNEL_ID)

    embd = discord.Embed(title="__Suggestion Recieved__", color=discord.Color.green())

    embd.add_field(
        name="Sent by",
        value=ctx.author.name,
        inline=False
    )
    
    embd.add_field(
        name="Sent from",
        value=ctx.guild.name,
        inline=False
    )
    embd.add_field(
        name="Suggestion",
        value=" ".join(text),
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    await suggestion_channel.send(embed=embd)

# returns the donation embed
async def get_donation_embed() -> discord.Embed:

    embd = await general_helper.get_info_embd(title="Support Aerial Ace", desc="")

    embd.description += f"{config.BULLET_EMOJI} **TIER-3 : **\n"

    embd.description += "Fully customizable starboard text! \n_You can now update the text of rare catch embed, and say a lot of things whether it be something more than Congrats, or straight out ask for its stats._\n\n"

    embd.description += f"{config.BULLET_EMOJI} **TIER-2 : **\n"
    embd.description += "Fully customizable starboard image. \n_Server of this tier will get access to custom starboard rare/shiny catch image. Update it to your server mascot or pick a good anime gif, and slap it in, the choice is yours._\n"
    embd.description += "Include rewards from the previous tiers.\n\n"

    embd.description += f"{config.BULLET_EMOJI} **TIER-1 : **\n"
    embd.description += "Fully [ We mean FULLY ] customizable starboard embed. \n_Servers of this tier have full control over how the starboard embed should look like. You can add custom invite links, vote links, messages, ask the users to perform certain task on catching a rare/shiny [ Good for events ] and what not. Definitely the most powerful and good for servers with a lot of events happening._\n"
    embd.description += "Includes rewards from the previous tiers\n\n"

    embd.description += "**To check the pricing, visit our patreon page.**\n\n"

    embd.description += "__By becoming a member of these tiers, you directly support the development of Aerial Ace. The base functionality of aerial-ace is and will always be 100% free. These customizations are just a way to thank our awesome supporters who keep the bot alive.__"

    return embd