"use strict";

var syllables = require("syllable")
var masterSyllables = require("../data/syllables.json");

var numberToText = require("number-to-text");
require('number-to-text/converters/en-us'); 

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

		// Check for digits and properly split them out, 
		// then convert from digit to text.
		if(word.match(/\d+/g)) {
			var splitDigits = word.match(/[a-zA-Z]+|[0-9]+/g);
			var stringifiedDigits = "";

			for(var j = 0; j < splitDigits.length; j++)
			{
				// Assume a trailing s means that the digits before it 
				// are pluralized, but only if it's the only other token
				if(splitDigits.length == 2 && j == 1 && splitDigits[j].match(/[sS]/g)) {
					stringifiedDigits += splitDigits[j];
				} else if(splitDigits[j].match(/\d+/g)) { 
					stringifiedDigits += numberToText.convertToText(splitDigits[j]);
				} else {
					stringifiedDigits += " " + splitDigits[j];
				}
			}
			
			count += syllables(stringifiedDigits);
		} 
		// Check the Moby project first because robots are bad at english.
		// If it's not in the dictionary, ask Zoltar.
		else if(word in masterSyllables) {
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
			break;
		} else if(count == 12) {
			line2 = true;
			result += "*\n*";
		} else if(count > 12 && !line2) {
			break;
		} else if(count > 17) {
			break;
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
