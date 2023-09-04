from discord import Interaction, TextChannel
from discord.interactions import Interaction
from discord.ui import InputText

import discord

class ThanksModal(discord.ui.Modal):

    previous_text:str = ""
    log_channel:TextChannel = None

    def __init__(self, previous_text:str, log_channel:TextChannel) -> None:

        super().__init__(title="Thanks for helping Aerial Ace!", timeout=200)

        self.previous_text = previous_text
        self.log_channel = log_channel

        self.add_item(
            InputText(label="Additional Comments?", style=discord.InputTextStyle.long)
        )

    async def callback(self, interaction: Interaction):
        
        self.previous_text += f"\n**Additional Comments** : {self.children[0].value or None}"

        


class SurveyModal(discord.ui.Modal):
    """Base Class to collect survey answers"""

    def __init__(self) -> None:
        super().__init__(title="Survey - Page 1 of 2", timeout=200)

        self.add_item(InputText(label="Question 1", style=discord.InputTextStyle.long, placeholder="Which Aerial Ace feature do you use the most?", required=True, min_length=5))
        self.add_item(InputText(label="Question 2", style=discord.InputTextStyle.long, placeholder="Is there any feature you feel is missing from Aerial Ace?", required=True))
        self.add_item(InputText(label="Question 3", style=discord.InputTextStyle.long, placeholder="Do you know that Aerial Ace has a premium version with more features?", required=True))
        self.add_item(InputText(label="Question 4", style=discord.InputTextStyle.long, placeholder="Have you joined the support server? If yes, how do you feel there?", required=True))
        self.add_item(InputText(label="Question 5", style=discord.InputTextStyle.long, placeholder="Do you check the mail command to get latest updates about new features?", required=True))

    async def callback(self, interaction: Interaction) -> None:

        survey_channel: TextChannel = interaction.client.get_channel(1148280621995659407)

        text  = f"# {interaction.user.mention}'s response from [{interaction.guild.name}](https://top.gg/servers/{interaction.guild.id})\n"
        text += f"Display Name : {interaction.user.name}\n\n"

        text += "**Question 1** : Which Aerial Ace feature do you use the most?\n"
        text += f"**Answer    ** : {self.children[0].value}\n\n"

        text += "**Question 2** : Is there any feature you feel is missing from Aerial Ace?\n"
        text += f"**Answer    ** : {self.children[1].value}\n\n"

        text += "**Question 3** : Do you know that Aerial Ace has a premium version with more features?\n"
        text += f"**Answer    ** : {self.children[2].value}\n\n"

        text += "**Question 4** : Have you joined the support server? If yes, how do you feel there?\n"
        text += f"**Answer    ** : {self.children[3].value}\n\n"

        text += "**Question 5** : Do you check the mail command to get latest updates about new features?\n"
        text += f"**Answer    ** : {self.children[4].value}\n\n"

        await survey_channel.send(text)

        await interaction.response.send_message("Thanks for submitting the survey! Your help makes aerial ace a better bot for everyone!", ephemeral=True)