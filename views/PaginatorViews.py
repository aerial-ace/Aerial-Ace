from discord import ButtonStyle
from discord.ext import pages

from config import FIRST_EMOJI, LAST_EMOJI, NEXT_EMOJI, PREV_EMOJI

class PageView(pages.Paginator):

    def __init__(self, paginator_pages):

        buttons = []

        first_button:pages.PaginatorButton = pages.PaginatorButton("first", None, FIRST_EMOJI, ButtonStyle.blurple)
        prev_button:pages.PaginatorButton = pages.PaginatorButton("prev", None, PREV_EMOJI, ButtonStyle.green)
        next_button:pages.PaginatorButton = pages.PaginatorButton("next", None, NEXT_EMOJI, ButtonStyle.green)
        last_button:pages.PaginatorButton = pages.PaginatorButton("last", None, LAST_EMOJI, ButtonStyle.blurple)

        buttons.append(first_button)
        buttons.append(prev_button)
        buttons.append(next_button)
        buttons.append(last_button)

        super().__init__(paginator_pages, custom_buttons=buttons, show_indicator=False, use_default_buttons=False)

def get_paginator_from_embeds(embeds:list, loopable=False):

    paginator = pages.Paginator(pages=embeds, loop_pages=loopable)

    return paginator
        