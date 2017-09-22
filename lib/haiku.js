"use strict";

var syllables = require("syllable");

async function haiku(logger, client, user, userID, channelID, message) {
	var words = message.split(" ");

	var count = 0
	var line1 = false;
	var line2 = false;
	var line3 = false;
	var result = "*"

	for(var i = 0; i < words.length; i++)
	{
		count += syllables(words[i]);
		result += words[i];

		if(words[i].includes("sed")
			|| words[i].includes("shed")
			|| words[i].includes("wed")
			|| words[i].includes("xed")) {
			// syllable has issues with these suffixes -
			// until the problem is fixed, manually decrement.
			count--;
		}

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
