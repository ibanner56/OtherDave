import discord
import random
from otherdave.commands.ignore import canDm
from otherdave.util import config

async def haunt(interaction: discord.Interaction, user: discord.Member) -> None:
    target = user or interaction.author
    if (canDm(target.id)):
        channel = await target.create_dm()
        f = random.choice(["doot_intensifies.png", "skelly_gun.gif", "oh_no.png", "skelly_dance.gif", "skelly_daddy.png", "doot.png", "education.png"])
        m = random.choice(["HAHA get haunted punk", "Someone wanted me to haunt you **real** bad", "Uh oh! Haunting incoming!", "Hi, I brought you this :)", "I'm very lost right now", 
        "Wow being a dead bot is a really odd experience, I can't feel my toes, I'M NOT SURE I EVEN HAVE TOES!"])
        await channel.send(m, file=discord.File("images/" + f))
        await interaction.response.send_message(config.emotions["_hauntmoji"], ephemeral=True)
    else:
        await interaction.message.send_message(config.emotions["_prohibited"], ephemeral=True)