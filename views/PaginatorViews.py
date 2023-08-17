from discord import ButtonStyle
from discord.ext import pages
from discord.ext.pages import PaginatorButton

from config import PREV_EMOJI, NEXT_EMOJI, FIRST_EMOJI, LAST_EMOJI


class PageView(pages.Paginator):

    def __init__(self, pages: list, show_all_btns: bool = False):

        prev_btn: PaginatorButton = PaginatorButton(
            "prev", None, PREV_EMOJI, ButtonStyle.gray)
        next_btn: PaginatorButton = PaginatorButton(
            "next", None, NEXT_EMOJI, ButtonStyle.gray)
        first_btn: PaginatorButton = PaginatorButton(
            "first", None, FIRST_EMOJI, ButtonStyle.gray)
        last_btn: PaginatorButton = PaginatorButton(
            "last", None, LAST_EMOJI, ButtonStyle.gray)

        buttons = []

        if show_all_btns:
            buttons.append(first_btn)

        buttons.append(prev_btn)
        buttons.append(next_btn)

        if show_all_btns:
            buttons.append(last_btn)

        for i in range(len(pages)):
            pages[i].set_footer(text=f"Page {i+1} of {len(pages)}")

        super().__init__(
            pages,
            loop_pages=True,
            disable_on_timeout=True,
            show_indicator=False,
            show_disabled=True,
            use_default_buttons=False,
            custom_buttons=buttons,
            timeout=30
        )
