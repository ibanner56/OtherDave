"use strict";

var randy = require("randy");
var fs = require("fs");

var adjectives = require("../data/prompt/adjectives.json");
var nouns = require("../data/prompt/nouns.json");

async function drawPrompt(logger, client, user, userID, channelID, args) {
	logger.info("Prompt - user: " + user + ", args: " + args);
	
	if(args.length > 1 && args[0] == "-forget") {
		if(adjectives.includes(args[1])) {
			delete adjectives[args[1]];
			fs.writeFile(
				"./data/prompt/adjectives.json",
				JSON.stringify(adjectives),
				function(error) {
					if(error) {
						logger.error(error);
					}
				});
		}
		
		if(nouns.includes(args[1])) {
			delete nouns[args[1]];
			fs.writeFile(
				"./data/prompt/nouns.json",
				JSON.stringify(nouns),
				function(error) {
					if(error) {
						logger.error(error);
					}
				});
		}

		client.sendMessage({
			to: channelID,
			message: "Okay, " + user + ", I forgot " + args[1]
		});
	} else {
		client.sendMessage({
			to: channelID,
			message: randy.choice(adjectives) 
				+ " " + randy.choice(nouns)
		});
	}
}

module.exports = drawPrompt;
