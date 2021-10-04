import discord
import random
import yaml

with open("./conf.yaml", encoding="utf-8") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)

async def spook(ctx, user):
    target = user or ctx.author
    channel = await target.create_dm()
    f = random.choice(["doot_intensifies.png", "intense_spook.png", "oh_no.png", "spooky_scary.gif", "spooky_time.png", "spook.png"])
    m = random.choice(["HAHA get spooked punk", "Someone wanted to spook you **real** bad", "Uh oh! Spook incoming!", "Hi, I brought you this :)", "I'm very lost right now"])
    await channel.send(m, file=discord.File("images/" + f))
    await ctx.message.add_reaction(config["emotions"]["_spookmoji"])
