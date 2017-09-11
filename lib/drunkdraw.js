"use strict";

var moment = require("moment");
var fs = require("fs");

function drunkdraw(logger, user, message) {
    logger.info("DrunkDraw - user: " + user + ", message: " + message);

    var args = message.split(" ").slice(1);
    if(args.length > 0) {
    	logger.debug(args);
		if(user != "MercWorks"){
			return "Mama Mia! Only Dave can do that!";
		}
    }
    else {
	  	var drawfile = fs.readFileSync("./otherdave/drunkdraw.json", "utf8");
		var draw = JSON.parse(drawfile);
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
