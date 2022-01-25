import discord
import random

import config

# returns a value for roll
async def roll(max_value, user) -> str:

    if max_value < 0:
        return f"> **{user.name}** rolled and got ||Nothing|| :]"

    random_value = random.randint(0, max_value)
    return f"> **{user.name}** rolled and got {random_value} :game_die: [0 - {max_value}]"

# returns the about the bot embed
async def get_about_embed() -> discord.Embed:
    embd = discord.Embed(title="__ABOUT - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = "Aerial Ace = Pokedex + Poketwo Helper Bot"

    embd.add_field(
        name="Prefix",
        value="`-aa ` and `@AerialAce`",
        inline=True
    )
    embd.add_field(
        name="Support Server",
        value=f"[Click here]({config.SUPPORT_SERVER_LINK})",
        inline=True
    )
    embd.add_field(
        name="Vote Link",
        value=f"[Click Here]({config.VOTE_LINK})",
        inline=True
    )

    embd.add_field(
        name="Source Details",
        value=f"Aerial Ace is an open source project released under GNU GPL v3 license.\nComplete source of the project is available [here]({config.REPO_LINK}).\nRepo stars are appreciated :3",
        inline=False
    )

    embd.add_field(
        name="Made with <3 by **DevGa.me**",
        value=f"**Discord** : `DevGa.me#0176`\n**Github** : [Devanshu19]({config.GITHUB_PROFILE_LINK})",
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# returns the vote embed
async def get_vote_embed() -> discord.Embed:
    embd = discord.Embed(title="__Vote for Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"You can help Aerial Ace by voting for it [here]({config.VOTE_LINK})\n**Thank you** if you voted :3"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# returns the support server embed
async def get_support_server_embed() -> discord.Embed:
    embd = discord.Embed(title="__Support Server__", color=config.NORMAL_COLOR)
    embd.description = f"Join the support server for reporting bugs, suggesting features,\ngetting help...you got it.\n\n[Click here to join]({config.SUPPORT_SERVER_LINK})"
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

# returns the invite embed
async def get_invite_embed() -> discord.Embed:
    embd = discord.Embed(title="__Invite - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"[Click Here]({config.INVITE_LINK}) to invite Aerial Ace to your server."
    embd.add_field(
        name = ":warning: NOTE :",
        value = "Aerial Ace is going through official verification process and before verification, the max server the bot can join is 100. \nSo if you are unable to invite, it is because of that. \nDw though, the links will start working once the verification is done. \nSorry for inconvenience ):",
        inline=False
    )
    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd