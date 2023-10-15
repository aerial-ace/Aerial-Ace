from discord import ButtonStyle, Interaction
from discord.ui import View, Button

from views.ModalViews import SurveyModal
from helpers import general_helper
from config import PATREON_EMOJI, PAYPAL_EMOJI, KO_FI_EMOJI, PREMIUM_EMOJI, PATREON_LINK, PAYPAL_LINK, INVITE_LINK, SUPPORT_SERVER_LINK, REPO_LINK, VOTE_LINK, GITHUB_EMOJI, GITHUB_SPONSORS_LINK, KO_FI_LINK


class DonationView(View):

    def __init__(self, timeout: int):
        super().__init__()

        self.timeout = timeout

        paypal_btn = Button(label="PayPal", emoji=PAYPAL_EMOJI, style=ButtonStyle.link, url=PAYPAL_LINK)
        patreon_btn = Button(label="Patreon", emoji=PATREON_EMOJI, style=ButtonStyle.link, url=PATREON_LINK)
        ko_fi_btn = Button(label="Ko-Fi", emoji=KO_FI_EMOJI, style=ButtonStyle.link, url=KO_FI_LINK)
        github_btn = Button(label="Github Sponsors", emoji=GITHUB_EMOJI, style=ButtonStyle.link, url=GITHUB_SPONSORS_LINK)

        self.add_item(patreon_btn)
        self.add_item(ko_fi_btn)
        self.add_item(paypal_btn)
        self.add_item(github_btn)


class AcceptanceView(View):
    acceptance_callback = None
    decline_callback = None

    context = None

    def __init__(self, timeout: int, context, accept_callback, decline_callback):

        super().__init__()

        self.timeout = timeout

        accept_btn = Button(label="Accept", style=ButtonStyle.green)
        decline_btn = Button(label="Decline", style=ButtonStyle.gray)

        self.acceptance_callback = accept_callback
        self.decline_callback = decline_callback
        self.context = context

        accept_btn.callback = self.acceptance_callback_main
        decline_btn.callback = self.decline_callback_main

        self.disable_on_timeout = True

        self.add_item(accept_btn)
        self.add_item(decline_btn)

    async def acceptance_callback_main(self, interaction: Interaction):

        await interaction.response.defer()

        if interaction.user != self.context.author:
            return await interaction.response.send_message("This is not your command!", ephemeral=True)

        result = await self.acceptance_callback(interaction)

        if result:
            self.disable_all_items()

            await interaction.message.edit(view=self)

    async def decline_callback_main(self, interaction: Interaction):

        await interaction.response.defer()

        if interaction.user != self.context.author:
            return await interaction.response.send_message("This is not your command!", ephemeral=True)

        result = await self.decline_callback(interaction)

        if result:
            self.disable_all_items()

            await interaction.message.edit(view=self)


class GeneralView(View):

    def __init__(self, timeout: int = 200, invite: bool = True, support_server: bool = True, source: bool = False, donate: bool = True, vote=False, survey=True):

        super().__init__()

        self.timeout = timeout

        invite_button: Button = Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link)
        support_server_button: Button = Button(label="Support Server", url=SUPPORT_SERVER_LINK, style=ButtonStyle.link)
        source_button: Button = Button(label="Source Code", url=REPO_LINK, style=ButtonStyle.link)
        vote_button: Button = Button(label="Vote", style=ButtonStyle.link, url=VOTE_LINK)
        premium_button: Button = Button(label="Premium", style=ButtonStyle.gray, emoji=PREMIUM_EMOJI)
        premium_button.callback = self.donate_callback
        survey_button: Button = Button(label="Take a short survey", style=ButtonStyle.gray, emoji="✉️")
        survey_button.callback = self.survey_callback

        if invite:
            self.add_item(invite_button)
        if support_server:
            self.add_item(support_server_button)
        if source:
            self.add_item(source_button)
        if vote:
            self.add_item(vote_button)
        if donate:
            self.add_item(premium_button)
        # if survey:
        #     self.add_item(survey_button)

    async def donate_callback(self, interaction: Interaction) -> None:

        embd = await general_helper.get_info_embd(
            title="Aerial Ace Premium",
            desc="Thanks for checking out the Premium Module.\nSubscribe to our patreon or paypal to avail premium features and support the development of Aerial Ace",
            show_thumbnail=True
        )

        view = DonationView(2000)

        await interaction.response.send_message(embed=embd, view=view)

    async def survey_callback(self, interaction: Interaction) -> None:

        await interaction.response.send_modal(SurveyModal())