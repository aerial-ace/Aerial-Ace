from multiprocessing.spawn import import_main_path
from discord import ButtonStyle
from discord.ui import View, Button
from discord.ext import pages

from config import INVITE_LINK, SUPPORT_SERVER_LINK, VOTE_LINK, REPO_LINK, FIRST_EMOJI, LAST_EMOJI, NEXT_EMOJI, PREV_EMOJI

class GeneralView(View):

    def __init__(self, timeout:int, invite:bool=True, support_server:bool=True, vote:bool=False, source:bool=False):

        super().__init__()

        self.timeout = timeout

        invite_button : Button = Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link)
        support_server_button : Button = Button(label="Support Server", url=SUPPORT_SERVER_LINK, style=ButtonStyle.link)
        source_button : Button = Button(label="Source Code", url=REPO_LINK, style=ButtonStyle.link)
        vote_button : Button = Button(label="Vote", url=VOTE_LINK, style=ButtonStyle.link)

        if(invite):
            self.add_item(invite_button)
        if(support_server):
            self.add_item(support_server_button)
        if(source):
            self.add_item(source_button)
        if(vote):
            self.add_item(vote_button)

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
        