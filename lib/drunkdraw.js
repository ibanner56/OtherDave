"use strict";

var moment = require("moment");
var fs = require("fs");

function buildResponse(user, userID, args) {
	var drawfile = fs.readFileSync("./data/drunkdraw.json", "utf8");
	var draw = JSON.parse(drawfile);

    if(args.length > 0) {
		if(user != "Isaac" && user != "MercWorks"){
			return "Mama Mia! Only Dave can do that!";
		}

		for(var i = 0; i < args.length;) {
			var flag = args[i];
			if (flag.charAt(0) != "-") {
				return "Sorry, I don't understand.";
			}

			var param = "";
			while(++i < args.length && args[i].charAt(0) != "-") {
				param += args[i] + " ";
			}
			param = param.trim();

			switch (flag) {
                case "-date":
					draw.date = param;
					break;

                case "-time":
					draw.time = param;
					break;

				case "-theme":
					draw.theme = param;
					break;

				case "-references":
					draw.references = param === "true";
					break;
				
				case "-reset":
					draw.date = null;
					draw.time = null;
					draw.theme = null;
					draw.references = false;
					break;

				default:
					return "Sorry, I don't understand.";
					break;
			}
		}

		var drawjson = JSON.stringify(draw, null, "\t");
		fs.writeFile("./data/drunkdraw.json", drawjson, "utf8", function(err) {
			if (err) {
				logger.error(err);
			}
		});
    	
		return "Got it, thanks " + user + "!";
	}
    else {
		var base = "The next drunkdraw is ";

    	if (draw.date) {
            base += draw.date + " ";
    	} else {
            var today = moment();
            var drawdate = moment({year: today.year(), month: today.month()});
        
			if(drawdate.day() == 0) {
	    		drawdate.date(8);
			} else {
			    drawdate.date(drawdate.date() + 14 - drawdate.day() % 7);
			}

        	if (today.date() > drawdate.date()) {
           	 	drawdate.month(drawdate.month() + 1);
				drawdate.date(1)

				if(drawdate.day() == 0) {
					drawdate.date(8);
				} else {
            		drawdate.date(drawdate.date() + 14 - drawdate.day() % 7);
				}
        	}

        	base += drawdate.format("dddd[,] MMMM Do ");
    	}

    	base += "at ";

        let timeValue;
    	if (draw.time) {
            base += draw.time + " ";
            timeValue = draw.time;
    	} else {
            base += "4:00 pm PST. ";
            timeValue = "4:00 pm PST";
    	}

    	if (draw.theme) {
       	 	base += "The theme is " + draw.theme + ". ";
        	if (draw.references) {
            	base += "\nJust this once, references ARE allowed.";
        	} else {
            	base += "\nAs always, references are NOT allowed.";
        	}
    	} else {
        	base += "Theme is still tbd.";
        }

        base += getTimeString(timeValue);

    	return base;
	}
}


function getTimeString(value, locales)
{
    try
    {
        let timeString = "\r\nAdjusted times:\r\n";

        // locales based on IANA timezone database. Codes can be found here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        // for whatever reason, "US/Pacific", and the like, were throwing errors. 
        locales = locales ||
            {
                Pacific: "America/Los_Angeles",
                Mountain: "America/Denver",
                Central: "America/Chicago",
                Eastern: "America/New_York",
                London: "Europe/London",
                Grenich: "Etc/GMT+0"
            };

        let parsedTime = parseTimeString(value);
        //console.log(parsedTime);

        let workspaceDate = new Date();
        let workingDate = getLocalTime(parsedTime.timeZoneOffset, parsedTime.hours, parsedTime.minutes);
        workingDate.setHours(parsedTime.hours - (workingDate.getHours() - workspaceDate.getHours()));
        workingDate.setMinutes(parsedTime.minutes);

        //console.log(workingDate);

        for (let property in locales)
        {
            if (locales.hasOwnProperty(property))
            {
                let locale = locales[property];
                let localeTime = workingDate.toLocaleTimeString('en-US', { timeZone: locale, hour: '2-digit', minute: '2-digit', hour12: true })
                timeString += `${property} - ${localeTime} \r\n`;
                //console.log("%s - %s", property, localeTime);
            }
        }

        return timeString;
    }
    catch (exception)
    {
        console.error(exception);
        return value;
    }
}
function parseTimeString(value)
{
    let regex = /(\d+)[\.:](\d+)( (\w+))?( (\w+))?/g;
    let regexMatches = regex.exec(value);

    let hours = regexMatches[1];
    let minutes = regexMatches[2];
    let firstString = regexMatches[4];
    let secondString = regexMatches[6];

    let meridian = null;
    let timeZoneOffset = null;

    if (firstString != null && firstString.trim() != "")
    {
        let meridianTest = getMeridan(firstString);
        if (meridianTest != null)
        {
            meridian = meridianTest;
        }
        else
        {
            timeZoneOffset = getTimeZoneOffset(firstString);
        }
    }

    if (secondString != null && secondString.trim() != "")
    {
        let meridianTest = getMeridan(secondString);
        if (meridianTest != null)
        {
            meridian = meridianTest;
        }
        else
        {
            timeZoneOffset = getTimeZoneOffset(secondString);
        }
    }

    if (timeZoneOffset == null)
    {
        timeZoneOffset = '-8'; //assumes pacific time
    }

    if (meridian != null && meridian === "pm")
    {
        let hoursNumber = parseFloat(hours);
        hoursNumber += 12;
        hours = hoursNumber.toString();
    }

    return {
        hours: hours,
        minutes: minutes,
        meridian: meridian,
        timeZoneOffset: timeZoneOffset
    };
}
function getMeridan(value)
{
    let meridians = ['am', 'pm'];
    for (let i = 0; i < meridians.length; i++)
    {
        let meridian = meridians[i];
        if (value.toLowerCase() === meridians[i])
        {
            return meridian;
        }
    }
    return null;
}
function getTimeZoneOffset(value)
{
    let timeZones = { "-8": ['pt', 'pst', 'pdt'], "-7": ['mt', 'mst', 'mdt'], "-6": ['ct', 'cst', 'cdt'], "-5": ['et', 'est', 'edt'] };
    for (let property in timeZones)
    {
        if (timeZones.hasOwnProperty(property))
        {
            let zonesArray = timeZones[property]

            for (let i = 0; i < zonesArray.length; i++)
            {
                let zoneString = zonesArray[i];
                if (value.toLowerCase() === zoneString)
                {
                    return property;
                }
            }
        }
    }

    return "-8"; //assumes Pacific time
}
function getLocalTime(timeZoneOffset)
{
    let offset = parseInt(timeZoneOffset);
    let now = new Date();
    let utc = now.getTime() + (now.getTimezoneOffset() * 60 * 1000);
    let offsetDate = new Date(utc + (3600000 * offset));
    return offsetDate;
}

async function drunkdraw(logger, client, user, userID, channelID, args) {
	logger.info("DrunkDraw - user: " + user + ", args: " + args);
	var response = buildResponse(user, userID, args);
	logger.debug(response);
	client.sendMessage({
		to: channelID,
		message: response
	});
}

module.exports = drunkdraw;
