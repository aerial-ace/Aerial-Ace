from discord import ButtonStyle
from discord.ui import View, Button

from config import INVITE_LINK, SUPPORT_SERVER_LINK, VOTE_LINK, REPO_LINK

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

        