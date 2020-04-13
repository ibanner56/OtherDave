"use strict";

var moment = require("moment");
var fs = require("fs");
var tz = require("timezone/loaded");
var dlog = require("./lib/dlog.js");

function buildResponse(logger, client, user, userID, args) {
	var drawfile = fs.readFileSync("./data/drunkdraw.json", "utf8");
	var draw = JSON.parse(drawfile);
	dlog(client, draw);

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
				dlog(client, err);
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

        var timeValue;
    	if (draw.time) {
            timeValue = draw.time;
    	} else {
            timeValue = "3:00 pm PT";
		}
		
		dlog(client, timeValue)
		
		base += timeValue+ ". ";

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
		
		base += "\r\nWe're currently indulging in the velvet caress of Satan here: https://whereby.com/mercworks"
		base += getTimeString(drawdate.format("YYYY-MM-DD") + " " + moment(timeValue, ["h:mm A Z"]).format("HH:mm"));

    	return base;
	}
}

function getTimeString(value)
{
    try
    {
        var timeString = "\r\n\r\nAdjusted times:";
		var parsedTime = tz(value, "America/Los_Angeles");
        var locales =
        {
            Pacific: "America/Los_Angeles",
            Mountain: "America/Denver",
            Central: "America/Chicago",
            Eastern: "America/New_York",
            London: "Europe/London",
            Grenich: "UTC"
        };

        for (var property in locales)
        {
        	timeString += "\r\n" + property + " - " + tz(parsedTime, locales[property], "%-I:%M %p %Z");
        }

        return timeString;
    }
    catch (exception)
    {
        console.error(exception);
        return value;
    }
}

async function drunkdraw(logger, client, user, userID, channelID, args) {
	logger.info("DrunkDraw - user: " + user + ", args: " + args);
	var response = buildResponse(logger, client, user, userID, args);
	logger.debug(response);
	client.sendMessage({
		to: channelID,
		message: response
	});
}

module.exports = drunkdraw;
