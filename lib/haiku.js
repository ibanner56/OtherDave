"use strict";

var syllables = require("syllable")
var masterSyllables = require("../data/syllables.json");

async function haiku(logger, client, user, userID, channelID, message, debug) {
	var words = message.split(/\s/g);

	var count = 0
	var line1 = false;
	var line2 = false;
	var line3 = false;
	var result = "*";
	var debugResult = ""

	for(var i = 0; i < words.length; i++)
	{
		var word = words[i];

		// Check the Moby project first because robots are bad at english.
		// If it's not in the dictionary, ask Zoltar.
		if(word in masterSyllables) {
			count += masterSyllables[word];
		} else if(word.toLowerCase() in masterSyllables) {
			count += masterSyllables[word.toLowerCase()];
		} else {
			count += syllables(word);
		}
		result += word;

		debugResult += word + " - ";
		debugResult += count + "\n";

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

	if(debug) {
		client.sendMessage({
			to: channelID,
			message: debugResult
		});
	} else if(count == 17) {
		result += "*";
		client.sendMessage({
			to: channelID,
			message: result
		});	
	}
}

module.exports = haiku;
