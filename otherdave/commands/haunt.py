import discord
import random
import yaml

from .ignore import canDm

with open("./conf.yaml", encoding="utf-8") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)

async def haunt(ctx, user):
    target = user or ctx.author
    if (canDm(target.id)):
        channel = await target.create_dm()
        f = random.choice(["doot_intensifies.png", "skelly_gun.gif", "oh_no.png", "skelly_dance.gif", "skelly_daddy.png", "doot.png", "education.png"])
        m = random.choice(["HAHA get haunted punk", "Someone wanted me to haunt you **real** bad", "Uh oh! Haunting incoming!", "Hi, I brought you this :)", "I'm very lost right now", 
        "Wow being a dead bot is a really odd experience, I can't feel my toes, I'M NOT SURE I EVEN HAVE TOES!"])
        await channel.send(m, file=discord.File("images/" + f))
        await ctx.message.add_reaction(config["emotions"]["_hauntmoji"])
    else:
        await ctx.message.add_reaction(config["emotions"]["_prohibited"])