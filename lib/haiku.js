"use strict";

var nlp = require("nlp_compromise");
var syllables = require("nlp-syllables");
nlp.plugin(syllables);

async function haiku(logger, client, user, userID, channelID, message) {
	var m2 = nlp.term(message);
	var msyl = m2.syllables();

	var count = 0
	var line1 = false;
	var line2 = false;
	var line3 = false;
	var result = "*"

	for(var i = 0; i < msyl.length; i++)
	{
		count += msyl[i].length;
		result += msyl[i].join("");
		
		if(count == 5) {
			line1 = true;
			result += "*\n*";
		} else if(count > 5 && !line1) {
			return;
		} else if(count == 12) {
			line2 = true;
			result += "*\n*";
		} else if(count > 12 && !line2) {
			return;
		} else if(count > 17) {
			return;
		} else if(count != 17) {
			result += " ";
		}
	}

	if(count == 17) {
		result += "*";
		client.sendMessage({
			to: channelID,
			message: result
		});
	}
}

module.exports = haiku;
