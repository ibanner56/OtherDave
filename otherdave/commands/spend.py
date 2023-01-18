import discord
import random
from .give import checkout
from typing import Optional
from otherdave.util import Relicer, Thinger

class Store(discord.ui.View):
    def __init__(self, *, timeout: Optional[float] = 180, customer: Optional[discord.User] = None, webhook: Optional[discord.Webhook]) -> None:
        super().__init__(timeout=timeout)
        if (customer):
            self.customer = customer
        if (webhook):
            self.webhook = webhook

        self.relicer = Relicer()
        self.thinger = Thinger()

    @discord.ui.button(label="Standard Prize - ₫100", row=0, style=discord.ButtonStyle.grey, emoji="\U0001F6E1")
    async def standardprize(self, interaction:discord.Interaction, button:discord.ui.Button) -> None:
        button.disabled = True
        await interaction.response.edit_message(view=self)

        # 1/10 chance for a relic
        thing = random.choice([self.relicer, self.thinger, self.thinger, self.thinger, self.thinger, 
            self.thinger, self.thinger, self.thinger, self.thinger, self.thinger]).make()

        thing = self.thinger.standardifyThing(thing)
        confirmation = checkout(self.customer, thing, 100)
        await self.webhook.send(confirmation[1], ephemeral = not confirmation[0])

    @discord.ui.button(label="Rare Prize - ₫1000", row=0, style=discord.ButtonStyle.red, emoji="\U00002697")
    async def rareprize(self, interaction:discord.Interaction, button:discord.ui.Button) -> None:
        button.disabled = True
        await interaction.response.edit_message(view=self)

        # 1/5 chance for a relic
        thing = random.choice([self.relicer, self.thinger, self.thinger, self.thinger, self.thinger]).make()
        thing = self.thinger.rarifyThing(thing)
        confirmation = checkout(self.customer, thing, 1000)
        await self.webhook.send(confirmation[1], ephemeral = not confirmation[0])

    @discord.ui.button(label="Legendary Prize - ₫5000", row=1, style=discord.ButtonStyle.blurple, emoji="\U00002728")
    async def legendaryprize(self, interaction:discord.Interaction, button:discord.ui.Button) -> None:
        button.disabled = True
        await interaction.response.edit_message(view=self)

        thing = self.relicer.make()
        thing = self.thinger.legendarifyThing(thing)
        confirmation = checkout(self.customer, thing, 5000)
        await self.webhook.send(confirmation[1], ephemeral = not confirmation[0])

    @discord.ui.button(label="A Snack - ₫50", row=1, style=discord.ButtonStyle.green, emoji="\U0001F961")
    async def snack(self, interaction:discord.Interaction, button:discord.ui.Button) -> None:
        button.disabled = True
        await interaction.response.edit_message(view=self)

        thing = self.thinger.make()
        thing = self.thinger.foodifyThing(thing)
        confirmation = checkout(self.customer, thing, 50)
        await self.webhook.send(confirmation[1], ephemeral = not confirmation[0])