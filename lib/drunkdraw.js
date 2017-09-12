"use strict";

var moment = require("moment");
var fs = require("fs");

function drunkdraw(logger, user, message) {
    logger.info("DrunkDraw - user: " + user + ", message: " + message);
	var drawfile = fs.readFileSync("./data/drunkdraw.json", "utf8");
	var draw = JSON.parse(drawfile);

    var args = message.split(" ").slice(1);
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

		var drawjson = JSON.stringify(draw);
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
            base += draw.date;
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

    	if (draw.time) {
    	    base += draw.time;
    	} else {
    	    base += "4:00 pm PST. ";
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

    	return base;
	}
}

module.exports = drunkdraw;
