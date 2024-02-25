import logging
from datetime import *
import discord
from discord import AllowedMentions, activity, app_commands
from discord.ext import tasks, commands
from otherdave.commands import *
from otherdave.util import *
from typing import Literal, Optional

# Configure client
synced = False
quietTime = None
lastMsgTime = datetime.now()
otherotherdave = None
help_command = commands.DefaultHelpCommand(
    no_category = "Commands",
    command_not_found = constants.notFound)
client = commands.Bot(
    command_prefix = "!",
    description = config.description,
    help_command = help_command,
    intents=discord.Intents.all())

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./logs/otherdave.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# Configure tasks
@tasks.loop(seconds=int(config.parrotInterval))
async def squawk() -> None:
    try:
        await toucan(client, lastMsgTime, quietTime)
    except Exception as error:
        dlog(client, str(error))
        pass

# Configure commands
@client.tree.command(
    name="beach",
    description = "Fine, you wanted a beach - I made him a beach. Happy? Sheesh."
)
@app_commands.check(callerNotIgnored)
async def cmd_beach(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(jabber.beach())

@client.tree.context_menu(
    name="*Daddy*"
)
@app_commands.checks.cooldown(1, 60)
async def ctx_daddy(interaction: discord.Interaction, message: discord.Message) -> None:
    await interaction.response.send_message(message.content + ", *daddy*")

@client.tree.command(
    name = "dadjoke", 
    description="I tell dad jokes but I'm not a dad. Guess that makes me a faux pa.")
@app_commands.check(callerNotIgnored)
async def cmd_dad(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(jabber.dad())

@client.tree.command(
    name = "dms",
    description = "Disables direct messages from OtherDave, triggered by other users or otherwise."
)
async def cmd_dms(interaction: discord.Interaction, action: Literal["enable", "disable"]) -> None:
    await interaction.response.send_message(dms(interaction.user.id, action), ephemeral = True)

@client.tree.command(
    name = "drop",
    description = "Allows you to drop a non-davebucks thing you're carrying.",
)
@app_commands.describe(
    thing = "The item you want to drop"
)
@app_commands.check(callerNotIgnored)
async def cmd_drop(interaction:discord.Interaction, thing: str) -> None:
    await interaction.response.send_message(drop(interaction.author.mention, thing))

## TODO: Update drunkdraw to list guild events
async def cmd_drunkdraw(ctx, *args) -> None:
    await ctx.send(drunkdrawCmd(ctx, args))
    
@client.tree.command(
    name = "forget",
    description = "Forgets something that was recently quoted."
)
@app_commands.check(callerNotIgnored)
async def cmd_forget(interaction: discord.Interaction, snippet: str) -> None:
    await interaction.response.send_message(forget(snippet))

@client.tree.context_menu(
    name="Forget Message"
)
async def ctx_forget(interaction: discord.Interaction, message: discord.Message) -> None:
    response = forget_msg(message)
    await interaction.response.send_message(response, ephemeral=True)

@client.tree.command(
    name = "give",
    description = "Gives something *to* OD or takes something *from* OD and gives it to the target."
)
@app_commands.describe(
    thing = "If you're not feeling creative, leave this blank. Only Dave can give out DaveBucks."
)
@app_commands.check(callerNotIgnored)
async def cmd_give(interaction: discord.Interaction, target: Optional[discord.Member] = None, thing: Optional[str] = None) -> None:
    thing = thing if thing else "something"
    target = target if target else discord.Object(id=config.selfid)
    await interaction.response.send_message(give(interaction.user, target, thing))

@client.tree.command(
    name = "haiku",
    description = """*Prints out a haiku.* 
        *Can be used to debug them,* 
        *fix, save, or forget.*"""
)
@app_commands.rename(
    debugSnippet = "debug", 
    correctParams = "correct",
    saveSnippet = "save",
    forgetSnippet = "forget")
@app_commands.check(callerNotIgnored)
async def cmd_haiku(
    interaction: discord.Interaction, 
    debugSnippet: Optional[str] = None, 
    correctParams: Optional[str] = None, 
    saveSnippet: Optional[str] = None, 
    forgetSnippet: Optional[str] = None) -> None:

    await interaction.response.send_message(
        haiku.critique(
            debugSnippet,
            correctParams,
            saveSnippet,
            forgetSnippet
        ))

@client.tree.context_menu(
    name="Save Haiku"
)
async def ctx_haiku(interaction: discord.Interaction, message: discord.Message) -> None:
    response = await save_hku(message)
    await interaction.response.send_message(response, ephemeral=True)

@client.tree.command(
    name = "haunt",
    description = "Haunts a <@user> of your choosing, or yourself."
)
@app_commands.describe(
    user = "The boring lame-o who needs some spooky spice in their life, or you, shackled with ennui, if empty"
)
@app_commands.check(callerNotIgnored)
async def cmd_haunt(interaction: discord.Interaction, user: Optional[discord.Member] = None) -> None:
    await haunt(interaction, user)

@cmd_haunt.error
async def cmd_haunt_error(interaction: discord.Interaction, error: discord.DiscordException) -> None:
    if isinstance(error, commands.BadArgument):
        await interaction.response.send_message("OOPSIE, looks like that user doesn't exist, sad day for them whoever they are!", ephemeral=True)

@client.tree.command(
    name = "horoscope",
    description = "Gives you a horoscope, given a star sign."
)
@app_commands.describe(
    variant = "A star sign for a specific horoscope, or 'al' for a Weird Al horoscope"
)
@app_commands.check(callerNotIgnored)
async def cmd_horoscope(interaction: discord.Interaction, variant: Optional[str] = "generic") -> None:
    await interaction.response.send_message(horoscope(variant))

@client.tree.command(
    name = "ignore",
    description = "Stops listening to a user for a set time, or 5 minutes. They must have been naughty!"
)
@app_commands.describe(
    user = "Who needs ignoring, or you if you leave this blank",
    minutes = "How long they need to be ignored"
)
async def cmd_ignore(interaction: discord.Interaction, user: Optional[discord.User] = None, minutes: Optional[int] = 5) -> None:
    selfIgnore = user is None
    user = user if user else interaction.user
    await interaction.response.send_message(ignore(interaction, user, minutes), ephemeral=selfIgnore)

@client.tree.command(
    name = "inventory",
    description = "Lists everything in OtherDave's inventory. You can add or remove items with !give."
)
@app_commands.describe(
    user = "The user who's inventory you want to list, leave blank for OtherDave"
)
@app_commands.check(callerNotIgnored)
async def cmd_inventory(interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
    await interaction.response.send_message(inventory(interaction.user, user))

@client.tree.command(
    name = "lwys",
    description = "Creates a fake LWYS script, always beginning with stage direction.",
)
@app_commands.describe(
    cast = "The cast to use, from Fixit, Hattie, Oldie, Sophie, Todd, and Tomo. Chooses two at random if empty."
)
@app_commands.check(callerNotIgnored)
async def cmd_lwys(interaction: discord.Interaction, cast: Optional[str] = "") -> None:
    strip = None
    async with interaction.channel.typing():
        strip = lwys(re.split(r"[\s,;]+", cast))

    await interaction.response.send_message(strip)

@client.tree.context_menu(
    name="Mock User"
)
@app_commands.checks.cooldown(1, 60)
async def ctx_mock(interaction: discord.Interaction, message: discord.Message) -> None:
    await interaction.response.send_message(mock(message.content))

@client.tree.command(
    name = "parrot",
    description = "Repeats a saved quote at random for you or for a specific user."
)
@app_commands.describe(
    user = "Who to parrot, defaults to you if empty"
)
@app_commands.check(callerNotIgnored)
async def cmd_parrot(interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
    mention = user.mention if user else interaction.user.mention
    await interaction.response.send_message(parrot(mention), allowed_mentions=AllowedMentions(users=[otherotherdave]))

@client.tree.command(
    name = "pedant",
    description = "Enables or disables auto-responses from OtherDave, if you're grumpy and want him to leave you alone.",
)
async def cmd_pedant(interaction: discord.Interaction, action: Literal["enable", "disable"]) -> None:
    await interaction.response.send_message(grump(interaction, action), ephemeral=True)

@client.tree.command(
    name = "ping",
    description = "pong"
)
@app_commands.check(callerNotIgnored)
async def cmd_ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("pong")

@client.tree.command(
    name = "prompt",
    description = "Madlibs a writing prompt and can {verb} a {noun} or {verb} one too.",
)
@app_commands.rename(
    addParams = "add",
    forgetParams = "forget"
)
@app_commands.check(callerNotIgnored)
async def cmd_prompt(interaction: discord.Interaction, addParams: Optional[str] = None, forgetParams: Optional[str] = None) -> None:
    await interaction.response.send_message(prompt(addParams, forgetParams))

@client.tree.command(
    name = "quiet",
    description = "Disables all non-command triggers for a number of minutes. Defaults to 5 min.",
)
@app_commands.check(callerNotIgnored)
async def cmd_quiet(interaction: discord.Interaction, mins: Optional[int] = 5) -> None:
    global quietTime
    try:
        quietTime = datetime.now() + timedelta(minutes=mins)
        await interaction.response.send_message("Got it, I'll keep quiet for " + mins + " minutes.")
    except:
        await interaction.response.send_message("Sorry, not sure how long that is...defaulting to 5 min")
        quietTime = datetime.now() + timedelta(minutes=5)

@client.tree.command(
    name = "recommend",
    description = "Gives you a song or game recommendation based on what others have been enjoying."
)
@app_commands.check(callerNotIgnored)
async def cmd_recommend(interaction: discord.Interaction, kind: Optional[Literal["music", "games"]] = "music") -> None:
    await interaction.response.send_message(embed=recommend(kind))

@client.tree.command(
    name = "remember",
    description = "Saves something a user just said to quote later."
)
@app_commands.describe(
    member="The person who said that funny thing",
    snippet="A bit of that funny thing that funny person said"
)
@app_commands.check(callerNotIgnored)
async def cmd_remember(interaction: discord.Interaction, member:discord.Member, snippet: str) -> None:
    response = await remember(interaction, member, snippet)
    await interaction.response.send_message(content=response, ephemeral=True)

@client.tree.context_menu(
    name="Remember Message"
)
async def ctx_remember(interaction: discord.Interaction, message: discord.Message) -> None:
    response = await remember_msg(message)
    await interaction.response.send_message(response, ephemeral=True)

@client.tree.command(
    name = "respect",
    description = "Respects you or another specified target."
)
@app_commands.describe(
    user = "The glum chum who needs a pick-me-up",
    thing = "The rad chad you need OtherDave to stan"
)
@app_commands.check(callerNotIgnored)
async def cmd_respect(interaction: discord.Interaction, user: Optional[discord.Member] = None, thing: Optional[str] = None) -> None:
    if user and thing:
        await interaction.response.send_message(constants.tooMuchRespect)
        return

    target = user.mention if user else thing if thing else interaction.user.mention
    await interaction.response.send_message(respect(target))

@client.tree.command(
    name = "spend",
    description = "Gets rid of all those pesky davebucks."
)
async def cmd_spend(interaction: discord.Interaction) -> None:
    store = Store(customer=interaction.user, webhook = interaction.followup)
    await interaction.response.send_message(content = constants.storefrontMessage, view = store, ephemeral = True)

@client.tree.command(
    name = "sync",
    description = "Only Isaac can touch me there."
)
async def cmd_sync(interaction: discord.Interaction) -> None:
    if (interaction.user.id == config.isaacid):
        # Sync command tree
        global synced
        if (not synced):
            await client.tree.sync()
            synced = True
            await interaction.response.send_message("Oooh that felt good, thanks.")
        else:
            await interaction.response.send_message("I'm already synced, thanks.")
    else:
        await interaction.response.send_message("Ew, no thanks.")

@client.tree.command(
    name = "use",
    description = "Uses an object in your inventory, or tells OtherDave to use an object in his."
)
@app_commands.check(callerNotIgnored)
async def cmd_use(interaction: discord.Interaction, my: Optional[bool] = False, thing: Optional[str] = "something") -> None:
    await interaction.response.send_message(useCmd(interaction.user, my, thing))

@client.tree.command(
    name = "version",
    description = "Prints the current version of OtherDave.",
)
async def cmd_version(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(config.version)

@client.tree.command(
    name = "wallet",
    description = "Tells you how many DaveBucks you've got - I hope it's a whoooooole bunch!"
)
@app_commands.check(callerNotIgnored)
async def cmd_wallet(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(wallet(interaction.user))

# Command groups
class MimicCog(commands.GroupCog, name="mimic"):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    async def sendMimicResponse(self, interaction: discord.Interaction, lines: list[str]) -> None:
        if (len(lines) == 0):
            return

        await interaction.response.send_message(lines[0], allowed_mentions=AllowedMentions(users=[otherotherdave]))
        for line in lines[1:]:
            await interaction.followup.send(line, allowed_mentions=AllowedMentions(users=[otherotherdave]))

    @app_commands.command(
        name = "user",
        description = "Tries to talk like you or other users. Can fake a conversation."
    )
    async def cmd_mimic_user(self, interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
        lines = []
        async with interaction.channel.typing():
            lines += mimicUser(user if user else interaction.user)
            
        await self.sendMimicResponse(interaction, lines)

    @app_commands.command(
        name = "combo",
        description = "Mimics a combination of two users."
    )
    async def cmd_mimic_combo(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User) -> None:
        lines = []
        async with interaction.channel.typing():
            lines += mimicCombo(str(user1.id), str(user2.id))
            
        await self.sendMimicResponse(interaction, lines)

    @app_commands.command(
        name = "chat",
        description = "Imitates a conversation between two users"
    )
    async def cmd_mimic_chat(self, interaction: discord.Interaction, user1: discord.User, user2: discord.User) -> None:
        lines = []
        async with interaction.channel.typing():
            lines += mimicChat(user1, user2)
            
        await self.sendMimicResponse(interaction, lines)

    @app_commands.command(
        name = "haiku",
        description = "Sometimes produces coherent poetry."
    )
    async def cmd_mimic_haiku(self, interaction: discord.Interaction, user: Optional[discord.User] = None) -> None:
        lines = []
        async with interaction.channel.typing():
            lines += mimicHaiku(user if user else interaction.user)
            
        await self.sendMimicResponse(interaction, lines)

# Configure events
@client.event
async def on_ready() -> None:
    # Add command groups
    await client.add_cog(MimicCog(client))

    # Sync command tree
    global synced
    if (not synced):
        await client.tree.sync()
        synced = True

    global otherotherdave
    otherotherdave = await client.fetch_user(config.daveid)

    logger.debug("Logged in as {0.user}".format(client))
    await dlog(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")
    await squawk.start()

@client.event
async def on_message(message: discord.Message) -> None:
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
async def on_reaction_add(reaction: discord.Reaction, _) -> None:
    if(reaction.message.author != client.user):
        return
    if(reaction.count == 1 and reaction.emoji in config.rereactions):
        await reaction.message.channel.send(config.rereactions[reaction.emoji])

@client.event
async def on_presence_update(user: discord.Member, after: discord.Member) -> None:
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
