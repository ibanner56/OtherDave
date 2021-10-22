import pickledb
import yaml
from datetime import *
from dateutil.parser import *
from dateutil.tz import *

pttzinfo = {
    "PT": gettz("America/Los_Angeles"),
    "PDT": gettz("America/Los_Angeles"), 
    "PST": gettz("America/Los_Angeles")
}
default_date = datetime.combine(datetime.now(), time(0, tzinfo=gettz("America/Los_Angeles")))
drawDB = pickledb.load("./data/dd.db", True)
with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)
    drawConf = config["drunkdraw"]

def updateDraw(author, args):
    if(author != "Isaac" and author != "MercWorks"):
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
            drawDB.set("date", param)
        elif(flag == "-time"):
            drawDB.set("time", param)
        elif(flag == "-theme"):
            drawDB.set("theme", param)
        elif(flag == "-references"):
            drawDB.set("references", param == "true")
        elif(flag == "-reset"):
            drawDB.set("date", None)
            drawDB.set("time", None)
            drawDB.set("theme", None)
            drawDB.set("references", False)
        else:
            return "Sorry, I don't understand."

    return "Got it, thanks " + author + "!"

def getDraw():
    base = "The next drunkdraw is "
    drawdate = None

    if(drawDB.get("date")):
        base += drawDB.get("date") + " "
        drawdate = parse(drawDB.get("date"))
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
    if(drawDB.get("time")):
        timeValue = drawDB.get("time")
    else:
        timeValue = "3:00 pm PT"

    base += timeValue + ". "

    if(drawDB.get("theme")):
        base += "The theme is " + drawDB.get("theme") + ".\n"
        if(drawDB.get("references")):
            base += "Just this once, references ARE allowed.\n"
        else:
            base += "As always, references are NOT allowed.\n"
    else:
        base += "The theme is still tbd.\n"

    base += "We are currently indulging in the velvet caress of Satan here: https://whereby.com/mercworks"
    base += "\n\n" + getTimeZones(drawdate.strftime("%Y-%m-%d") + " " + parse(timeValue, tzinfos=pttzinfo, default=default_date).strftime("%H:%M %Z"))

    return base    

def getTimeZones(value):
    timeString = "Adjusted times:"
    parsedTime = parse(value, tzinfos=pttzinfo)

    for locale in drawConf["locales"]:
        timeString += "\n" + locale + " - " 
        timeString += parsedTime.astimezone(gettz(drawConf["locales"][locale])).strftime("%I:%M %p %Z")

    return timeString

def drunkdraw(ctx, args):
    if(len(args) == 0):
        return getDraw()
    else:
        return updateDraw(ctx.message.author.name, args)
