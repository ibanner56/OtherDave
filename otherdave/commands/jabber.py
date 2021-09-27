import random
import yaml
from sys import maxsize

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

_notFound = "Buddy, I think you need !help."
_joy = ["va-va-voom", "wheee", "whoopee", "woohoo", "yay", "yippee", "yowza"]
_version = "OtherDave is running version " + str(config["version"])
_usage = {
    "beach": """!beach
        Fine, you wanted a beach - I made him a beach. Happy? Sheesh.""",
    "drunkdraw": """!drunkdraw [[-date date] [-time time] [-theme theme] [-references references] | -reset]
        Announces the next drunkdraw. Dave and Isaac can configure the draw as well.""",
    "forget": """!forget [keywords]
        Forgets something that was recently quoted.""",
    "haiku": """!haiku [-debug [poem] | -correct word syllables | -save [keywords] | -forget [keywords]]
        *Prints out a haiku.* 
        *Can be used to debug them,* 
        *fix, save, or forget.*""",
    "help": """!help [command]
        Prints this message, or just the snippet for a single command.""",
    "lwys": """!lwys [character1 character2 ...
        Creates a fake LWYS script, always beginning with stage direction. If no characters are provided, two are chosen at random.
        The full cast includes Fixit, Hattie, Oldie, Sophie, Todd, and Tomo.]""",
    "mimic": """!mimic [<@user> | -combo <@user> <@user> | -chat <@user> <@user> | -haiku <@user>]
        Tries to talk like you or another user. Can mash two users together or fake a conversation. Sometimes produces coherent poetry.
        Try adams, austen, carroll, doyle, hemingway, melville, obama, plato, or thoreau for some fun.""",
    "parrot": """!parrot [<@user>]
        Repeats a saved quote at random or for a specific user.""",
    "pedant": """!pedant -me | -stop
        Enables or disables auto-responses from OtherDave, if you're a grump and want him to leave you alone.""",
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

async def beach(client, message, args):
    sand = random.randint(2, maxsize)
    joy = random.choice(_joy)
    return await message.channel.send("Today I'm on a beach with {} grains of sand, {}!".format(sand, joy))

async def botHelp(client, message, args):
    helpMsg = ""
    if(len(args) > 1):
        helpMsg += _version + "\n\n"
    for func in args:
        if(func.startswith("!")):
            func = func.lstrip("!")
        if(not func in _usage):
            return await message.channel.send(_notFound)
        helpMsg += _usage[func] + "\n"
    return await message.channel.send(helpMsg)

async def ping(client, message, args):
    return await message.channel.send("pong")

async def version(client, message, args):
    return await message.channel.send(_version)
