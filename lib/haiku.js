"use strict";

var syllables = require("syllable")
var masterSyllables = require("../data/syllables.json");

async function haiku(logger, client, user, userID, channelID, message) {
	var words = message.split(/\s/g);

	var count = 0
	var line1 = false;
	var line2 = false;
	var line3 = false;
	var result = "*"

	for(var i = 0; i < words.length; i++)
	{
		// Check the Moby project first because robots are bad at english.
		// If it's not in the dictionary, ask Zoltar.
		if(words[i] in masterSyllables) {
			count += masterSyllables[words[i]];
		} else {
			count += syllables(words[i]);
		}
		result += words[i];

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
