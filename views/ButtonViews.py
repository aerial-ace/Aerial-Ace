from discord import ButtonStyle, Interaction
from discord.ui import View, Button

from cog_helpers import general_helper
from config import PATREON_EMOJI, PAYPAL_EMOJI, PATREON_LINK, PAYPAL_LINK, INVITE_LINK, SUPPORT_SERVER_LINK, REPO_LINK, VOTE_LINK

class DonationView(View):

    def __init__(self, timeout:int):

        super().__init__()

        self.timeout = timeout

        paypal_btn = Button(label="PayPal", emoji=PAYPAL_EMOJI, style=ButtonStyle.link, url=PAYPAL_LINK)
        patreon_btn = Button(label="Patreon", emoji=PATREON_EMOJI, style=ButtonStyle.link, url=PATREON_LINK)

        self.add_item(patreon_btn)
        self.add_item(paypal_btn)

class GeneralView(View):

    def __init__(self, timeout:int, invite:bool=True, support_server:bool=True, source:bool=False, donate:bool=False):

        super().__init__()

        self.timeout = timeout

        invite_button : Button = Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link)
        support_server_button : Button = Button(label="Support Server", url=SUPPORT_SERVER_LINK, style=ButtonStyle.link)
        source_button : Button = Button(label="Source Code", url=REPO_LINK, style=ButtonStyle.link)
        donate_button : Button = Button(label="Donate", style=ButtonStyle.gray)
        donate_button.callback = self.donate_callback

        if(invite):
            self.add_item(invite_button)
        if(support_server):
            self.add_item(support_server_button)
        if(source):
            self.add_item(source_button)
        if(donate):
            self.add_item(donate_button)

    async def donate_callback(self, interaction:Interaction) -> None:

        embd = await general_helper.get_info_embd(
            title="Donate to support Aerial Ace",
            desc="Thanks for checking out the donation module. \nYou can donate or subscribe to patreon to support the development of aerial ace. \nCurrently, 100% of server expenses are on the developer, so even your smallest donations matter a lot.",
            show_thumbnail=True
        )

        view = DonationView(2000)

        await interaction.response.send_message(embed=embd, view=view)