import yaml

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

_version = "OtherDave is running version " + str(config["version"])
_usage = {
    "drunkdraw": """!drunkdraw [[-date date] [-time time] [-theme theme] [-references references] | -reset]
        Announces the next drunkdraw. Dave and Isaac can configure the draw as well.""",
    "forget": """!forget [keywords]
        Forgets something that was recently quoted.""",
    "haiku": """!haiku [-debug [poem] | -correct word syllables | -save [keywords] | -forget [keywords]]
        *Prints out a haiku.* 
        *Can be used to debug them,* 
        *fix, save, or forget.*""",
    "help": """!help [command]
        Prints this message, or just the snippet for a single command."""
    "mimic": """!mimic [<@user>]
        Tries to talk like you or another user.""",
    "parrot": """!parrot [<@user>]
        Repeats a saved quote at random or for a specific user.""",
    "ping": """!ping
        pong""",
    "prompt": """!prompt [-add {noun|adjective} word | -forget word]
        Madlibs a writing prompt and can {verb} a {noun} or {verb} one too.""",
    "quiet": """!quiet [mins]
        Disables all non-command triggers for a number of minutes. Defaults to 5 min.""",
    "remember": """!remember <@user> keywords
        Saves something a user just said to quote later.""",
    "respect": """!respect [<target>]
        Respects you or another target. Can target <@user>s.""",
    "version": """!version
        Prints the current version of OtherDave."""
}

async def botHelp(client, message, args):
    helpMsg = ""
    if(len(args) > 1):
        helpMsg += _version + "\n\n"
    helpMsg += "Usage:\n"
    for func in args:
        if(func.startswith("!")):
            func = func.lstrip("!")
        helpMsg += _usage[func] + "\n"
    return await message.channel.send(helpMsg)

async def ping(client, message, args):
    return await message.channel.send("pong")

async def version(client, message, args):
    return await message.channel.send(_version)