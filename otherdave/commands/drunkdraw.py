import yaml
from datetime import *
from dateutil.parser import *
from dateutil.tz import *

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)
    draw = config["drunkdraw"]

def updateDraw(author, args):
    if(author != "Isaac" and author != "Mercworks"):
        return "Mama Mia! Only Dave can do that!"

    i = 0
    while(i < len(args)):
        flag = args[i]
        i += 1
        if(not flag.startswith("-")):
            return "Sorry, I don't understand."
        
        param = ""
        while(i < len(args) and not args[i].startswith("-")):
            param += args[i] + " "
            i += 1
        param = param.strip()

        if(flag == "-date"):
            draw["date"] = param
        elif(flag == "-time"):
            draw["time"] = param
        elif(flag == "-theme"):
            draw["theme"] = param
        elif(flag == "-references"):
            draw["references"] = param == "true"
        elif(flag == "-reset"):
            draw["date"] = None
            draw["time"] = None
            draw["theme"] = None
            draw["references"] = False
        else:
            return "Sorry, I don't understand."

    config["drunkdraw"] = draw
    with open("./conf.yaml", "w") as conf:
        yaml.dump(config, conf, sort_keys=False)

    return "Got it, thanks " + author + "!"

def getDraw():
    base = "The next drunkdraw is "
    drawdate = None

    if(draw["date"]):
        base += draw["date"] + " "
        drawdate = parse(draw["date"])
    else:
        today = datetime.today()
        drawdate = date(today.year, today.month, 1)

        if(drawdate.weekday == 6):
            drawdate = drawdate.replace(day=8)
        else:
            dday = 15 - drawdate.isoweekday() % 7
            drawdate = drawdate.replace(day=dday)

        base += drawdate.strftime("%A, %B %d ")

    base += "at "

    timeValue = None
    if(draw["time"]):
        timeValue = draw["time"]
    else:
        timeValue = "3:00 pm"

    base += timeValue + ". "

    if(draw["theme"]):
        base += "The theme is " + draw["theme"] + ".\n"
        if(draw["references"]):
            base += "Just this once, references ARE allowed."
        else:
            base += "As always, references are NOT allowed"
    else:
        base += "The theme is still tbd.\n"

    base += "We are currently indulging in the velvet caress of Satan here: https://whereby.com/mercworks"
    base += "\n\n" + getTimeZones(drawdate.strftime("%Y-%m-%d") + " " + parse(timeValue, tzinfos=[gettz("America/Los_Angeles")]).strftime("%H:%M %Z"))

    return base    

def getTimeZones(value):
    timeString = "Adjusted times:"
    parsedTime = parse(value, tzinfos=[gettz("America/Los_Angeles")])

    for locale in draw["locales"]:
        timeString += "\n" + locale + " - " 
        timeString += parsedTime.astimezone(gettz(draw["locales"][locale])).strftime("%I:%M %p %Z")

    return timeString

async def drunkdraw(client, message, args):
    if(len(args) == 0):
        await message.channel.send(getDraw())
    else:
        await message.channel.send(updateDraw(message.author.name, args))