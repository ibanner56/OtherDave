import logging
import yaml
from datetime import *
from discord import AllowedMentions, activity
from discord.ext import tasks, commands
from otherdave.commands import *
from otherdave.util import *

# Configure client
with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

quietTime = None
lastMsgTime = None
otherotherdave = None
help_command = commands.DefaultHelpCommand(
    no_category = "Commands",
    command_not_found = helpNotFound)
client = commands.Bot(
    command_prefix = "!",
    description = config["description"],
    help_command = help_command,
    intents=discord.Intents.all())

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./logs/otherdave.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# Configure tasks
@tasks.loop(seconds=int(config["parrot_interval"]))
async def squawk():
    await toucan(client, lastMsgTime, quietTime)

# Configure commands
@client.command(
    brief = "Fine, you wanted a beach - I made him a beach. Happy? Sheesh.",
    help = "Fine, you wanted a beach - I made him a beach. Happy? Sheesh.",
    name="beach"
)
async def cmd_beach(ctx):
    await ctx.send(jabber.beach())

@client.command(
    brief = "I tell dad jokes but I'm not a dad.",
    help = "I tell dad jokes but I'm not a dad. Guess that makes me a faux pa.",
    name = "dadjoke"
)
async def cmd_dad(ctx):
    await ctx.send(jabber.dad())

@client.command(
    brief = "Disables direct messages.",
    help = "Disables direct messages from OtherDave, triggered by other users or otherwise.",
    name = "dms",
    usage = "<-enable | -disable>"
)
async def cmd_dms(ctx, flag = None):
    await ctx.send(dms(ctx.author.id, flag))

@client.command(
    name = "drunkdraw",
    help = "Announces the next drunkdraw. Dave and Isaac can configure the draw as well.",
    brief = "Announces the next drunkdraw.",
    usage = "[[-date date] [-time time] [-theme theme] [-references references] | -reset]"
)
async def cmd_drunkdraw(ctx, *args):
    await ctx.send(drunkdraw(ctx, args))
    
@client.command(
    brief = "Forgets something that was recently quoted.",
    help = "Forgets something that was recently quoted.",
    name = "forget",
    usage = "[keywords]"
)
async def cmd_forget(ctx, *args):
    await ctx.send(forget(args))

@client.command(
    brief = "Interacts with OtherDave's inventory.",
    help = """Gives something *to* @OtherDave, if he's the target, 
        or takes something *from* @OtherDave and gives it to the @<target>. If you're not feeling 
        creative, leave object blank or request 'something' and OD will be creative for you. 
        If you're not feeling generous, '!give me [<object>]' will give things to you instead of a <target>.
        Defaults to giving @OtherDave a random 'something'.""",
    name = "give",
    usage = "[<target> <object>]"
)
async def cmd_give(ctx, target: str = "<@" + config["self_id"] + ">", *thing):
    thing = "something" if len(thing) == 0 else " ".join(thing)
    await ctx.send(give( ctx.author.mention, target, thing))

@client.command(
    brief = "..... ....... .....",
    help = """*Prints out a haiku.* 
        *Can be used to debug them,* 
        *fix, save, or forget.*""",
    name = "haiku",
    usage = "[-debug [poem] | -correct word syllables | -save [keywords] | -forget [keywords]]"
)
async def cmd_haiku(ctx, *args):
    await ctx.send(haiku.critique(args))

@client.command(
    brief = "Haunts a user in DMs.",
    help = "Haunts a <@user> of your choosing, or yourself.",
    name = "haunt",
    usage = "[<target>]"
)
async def cmd_haunt(ctx, user: discord.Member = None):
    await haunt(ctx, user)

@cmd_haunt.error
async def cmd_haunt_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("OOPSIE, looks like that user doesn't exist, sad day for them whoever they are!")

@client.command(
    brief = "Gives you a damn fine horoscope.",
    help = "Gives you a horoscope, you can provide a star sign or place the word 'al' after command to recieve a Weird Al horoscope.",
    name = "horoscope",
    usage = "[starsign | al]"
)
async def cmd_horoscope(ctx, variant: str = "generic"):
    await ctx.send(horoscope(variant))

@client.command(
    brief = "Stop listening to a user.",
    help = "Stops listening to a user for a set time, or 5 minutes. They must have been naughty!",
    name = "ignore",
    usage = "<-me | @user> [minutes]"
)
async def cmd_ignore(ctx, *args):
    response = await ignore(ctx, args)
    if (response):
        await ctx.send(response)

@client.command(
    brief = "Lists everything OtherDave is holding.",
    help = "Lists everything in OtherDave's inventory. You can add or remove items with !give.",
    name = "inventory"
)
async def cmd_inventory(ctx, user: str = None):
    await ctx.send(inventory(ctx.author.mention, user))

@client.command(
    brief = "Creates a fake LWYS script.",
    help = """Creates a fake LWYS script, always beginning with stage direction. If no characters are provided, two are chosen at random.
        The full cast includes Fixit, Hattie, Oldie, Sophie, Todd, and Tomo.]""",
    name = "lwys",
    usage = "[character1 [character2 ...]]"
)
async def cmd_lwys(ctx, *args):
    strip = None
    async with ctx.channel.typing():
        strip = lwys(args)

    await ctx.send(strip)

@client.command(
    brief = "Tries to talk like you or another user.",
    help = """Tries to talk like you or another user. Can mash two users together or fake a conversation. Sometimes produces coherent poetry.
        Try adams, austen, carroll, doyle, hemingway, melville, obama, plato, or thoreau for some fun.""",
    name = "mimic",
    usage = "[<@user> | -combo <@user> <@user> | -chat <@user> <@user> | -haiku [<@user>]]"
)
async def cmd_mimic(ctx, *args):
    lines = []
    async with ctx.channel.typing():
        lines += mimic(ctx, args)

    for line in lines:
        await ctx.send(line, allowed_mentions=AllowedMentions(users=[otherotherdave]))

@client.command(
    brief = "Repeats a saved quote.",
    help = "Repeats a saved quote at random or for a specific user.",
    name = "parrot",
    usage = "[<@user>]"
)
async def cmd_parrot(ctx, *args):
    await ctx.send(parrot(args), allowed_mentions=AllowedMentions(users=[otherotherdave]))

@client.command(
    brief = "Enables or disables auto-responses from OtherDave.",
    help = "Enables or disables auto-responses from OtherDave, if you're a grump and want him to leave you alone.",
    name = "pedant",
    usage = "-me | -stop"
)
async def cmd_pedant(ctx, *args):
    response = await grump(ctx, args)
    if (response):
        await ctx.send(response)

@client.command(
    brief = "pong",
    help = "pong",
    name = "ping"
)
async def cmd_ping(ctx):
    await ctx.channel.send("pong")

@client.command(
    brief = "Madlibs a writing prompt.",
    help = "Madlibs a writing prompt and can {verb} a {noun} or {verb} one too.",
    name = "prompt",
    usage = "[-add {noun|adjective} word | -forget word]"
)
async def cmd_prompt(ctx, *args):
    await ctx.channel.send(prompt(args))

@client.command(
    brief = "Disables all non-command triggers for a number of minutes.",
    help = "Disables all non-command triggers for a number of minutes. Defaults to 5 min.",
    name = "quiet",
    usage = "[mins]"
)
async def cmd_quiet(ctx, *args):
    global quietTime
    try:
        min = 5
        if(len(args)):
            min = int(args[0])

        quietTime = datetime.now() + timedelta(minutes=min)
        await ctx.send("Got it, I'll keep quiet for " + args[0] + " minutes.")
    except:
        await ctx.send("Sorry, not sure how long that is...defaulting to 5 min")
        quietTime = datetime.now() + timedelta(minutes=5)

@client.command(
    brief = "Gives you a cool recommendation.",
    help = "Gives you a song or game recommendation based on what others have been enjoying.",
    name = "recommend",
    usage = "[-music | -games]"
)
async def cmd_recommend(ctx, kind: str = "-music"):
    await ctx.send(embed=recommend(kind))

@client.command(
    brief = "Saves something a user just said to quote later.",
    help = "Saves something a user just said to quote later.",
    name = "remember",
    usage = "<@user> keywords"
)
async def cmd_remember(ctx, *args):
    response = await remember(ctx, args)
    if (response):
        await ctx.send(response)

@client.command(
    brief = "Respects you or another target.",
    help = "Respects you or another target. Can target <@user>s.",
    name = "respect",
    usage = "[<target>]"
)
async def cmd_respect(ctx, *args):
    await ctx.send(respect(ctx, args))

@client.command(
    brief = "Prints the current version of OtherDave.",
    help = "Prints the current version of OtherDave.",
    name = "version"
)
async def cmd_version(ctx):
    await ctx.send(version())

# Configure events
@client.event
async def on_ready():
    global otherotherdave
    otherotherdave = await client.fetch_user(194865073943085056)

    logger.debug("Logged in as {0.user}".format(client))
    await dlog(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")
    await squawk.start()

@client.event
async def on_message(message):
    global lastMsgTime
    lastMsgTime = datetime.now()
    if message.author == client.user:
        return
    elif (shouldIgnore(message.author.id)):
        # otherdave is always listening...
        listen(message)
        return

    content = message.content
    if content.startswith("!"):
        command, *_ = content.lstrip("!").split(" ")
        logger.info(command + " - user: " + message.author.name)
        if command in client.all_commands:
            await client.process_commands(message)
        else:
            await message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")
    else:
        global quietTime
        if(quietTime and datetime.now() > quietTime):
            quietTime = None

        if(not quietTime):
            await haiku.detect(message)
            await react(message)
            await pedant(message)

        # otherdave is always listening...
        listen(message)

@client.event
async def on_reaction_add(reaction, _):
    if(reaction.message.author != client.user):
        return
    if(reaction.count == 1 and reaction.emoji in config["rereactions"]):
        await reaction.message.channel.send(config["rereactions"][reaction.emoji])

@client.event
async def on_presence_update(user, after):
    if (len(after.activities) != 1):
        return

    if (isinstance(after.activity, activity.Spotify)):
        playlist(user, after.activity)
    elif (isinstance(after.activity, activity.Game)):
        wishlist(user, after.activity)

if __name__ == "__main__":
    tokenFile = open("bot.tkn", "r")
    token = tokenFile.read()
    client.run(token)