from textwrap import TextWrapper

from discord import AutoShardedBot, Bot, Embed, Forbidden, Guild, NotFound, Thread
from discord.abc import GuildChannel, PrivateChannel

import config


# for wrapping text
def wrap_text(width: int, text: str):
    wrapped_text = ""
    wrapper = TextWrapper(width)
    text_lines = wrapper.wrap(text)
    for line in text_lines:
        wrapped_text += f"{line}\n"

    return wrapped_text


# returns an embed provided the data
async def get_info_embd(title: str, desc: str = "", color: int = config.NORMAL_COLOR, footer: str | None = None, show_thumbnail: bool = False):
    embd = Embed()

    embd.color = color
    embd.title = title
    embd.description = desc

    if footer is not None:
        _ = embd.set_footer(text=footer)

    if show_thumbnail is True:
        _ = embd.set_thumbnail(url=f"{config.AVATAR_LINK}")

    return embd


# returns an error embed provided the data
async def get_error_embd(title: str, desc: str = "", footer: str | None = None, show_thumbnail: bool = False):
    embd = Embed()

    embd.color = config.ERROR_COLOR
    embd.title = title
    embd.description = desc

    if footer is not None:
        _ = embd.set_footer(text=footer)

    if show_thumbnail is True:
        _ = embd.set_thumbnail(url=f"{config.AVATAR_LINK}")

    return embd


# returns an error embed provided the data
async def get_warning_embd(title: str, desc: str = "", footer: str | None = None, show_thumbnail: bool = False):
    embd = Embed()

    embd.color = config.WARNING_COLOR
    embd.title = title
    embd.description = desc

    if footer is not None:
        _ = embd.set_footer(text=footer)

    if show_thumbnail is True:
        _ = embd.set_thumbnail(url=f"{config.AVATAR_LINK}")

    return embd


async def get_user_id_from_ping(ping: str) -> str:
    user_id = ping

    ping_chars = ["<", "!", "@", ">"]
    for char in ping_chars:
        user_id = user_id.replace(char, "")

    return user_id


async def get_trade_value(pokecoins: int, shinies: int, rares: int, redeems: int) -> int:
    return int(pokecoins) + config.TRADE_ITEM_WEIGHT["shinies"] * int(shinies) + config.TRADE_ITEM_WEIGHT["rares"] * int(rares) + config.TRADE_ITEM_WEIGHT["redeems"] * int(redeems)


# Sends a support reminder ever so often
async def donation_reminder() -> Embed:
    """Render the progress bar"""
    donation_goal_progress_percentage = 43

    empty_chunks = [config.EMPTY_START_EMOJI] + [config.EMPTY_MIDDLE_EMOJI] * 8 + [config.EMPTY_END_EMOJI]

    number_of_loading_bar_chunks = int(donation_goal_progress_percentage / 10)

    for i in range(number_of_loading_bar_chunks):
        if i == 0:
            empty_chunks[0] = config.FILLED_START_EMOJI
        elif i == 9:
            empty_chunks[9] = config.FILLED_END_EMOJI
        else:
            if i == number_of_loading_bar_chunks - 1:
                empty_chunks[i] = config.FILLED_MID_EMOJI
            else:
                empty_chunks[i] = config.FILLED_INTERMEDIATE_EMOJI

    embd = Embed(title="Help Aerial Ace", color=config.NORMAL_COLOR, description="Aerial Ace depends on its users to stay alive. \n\nTo keep the bot running smoothly, I could use some support through donations. Every little bit helps! You also get perks for your generosity! \n## Current Progress \n{} {}%".format("".join(empty_chunks), donation_goal_progress_percentage))

    # Yes, I hard coded the link.
    embd.set_thumbnail(url="https://i.imgur.com/cYQMCLw.gif")

    return embd


async def get_guild_from_bot(bot: Bot | AutoShardedBot, guild_id: int) -> Guild | None:
    """
    Try to get a guild from bot's memory cache and if not found then fetch the API directly.
    """

    # Fetch from the cache
    guild: Guild | None = bot.get_guild(guild_id)
    if guild is not None:
        return guild

    # Fetch from the API
    try:
        guild = await bot.fetch_guild(guild_id)
    except Exception:  # noqa: BLE001
        return None

    return guild


async def get_channel_from_bot(bot: Bot | AutoShardedBot, channel_id: int) -> GuildChannel | PrivateChannel | Thread | None:
    """
    Try to get a channel from bot's memory cache and if not found then fetch the API directly.
    """

    # Fetch from the cache
    channel: GuildChannel | PrivateChannel | Thread | None = bot.get_channel(int(channel_id))
    if channel is not None:
        return channel

    # Fetch from the API
    try:
        channel = await bot.fetch_channel(channel_id)
    except (NotFound, Forbidden):
        return None

    return channel


async def get_channel_from_server(server: Guild, channel_id: int) -> GuildChannel | PrivateChannel | Thread | None:
    """
    Try to get a channel from guild's memory cache and if not found then fetch the API directly.
    """

    # Fetch from the cache
    channel: GuildChannel | PrivateChannel | Thread | None = server.get_channel(channel_id)
    if channel is not None:
        return channel

    # Fetch from the API
    try:
        channel = await server.fetch_channel(channel_id)
    except (NotFound, Forbidden):
        return None

    return channel
