"use strict"

var fs = require("fs");
var markov = require("js-markov");

async function mimic(logger, client, user, userID, channelID, args) {
	logger.info("Mimic - user: " + user + ", args: " + args);
	
	client.simulateTyping(channelID);

	var person = userID;
	if(args.length > 0) {
		person = args[0].replace(/<@!*|>/g, "");
	}

	fs.readFile("./data/markov/" + person + ".txt", function(error, data) {
		if(error) {
			logger.error(error);
			return;
		}
		
		// Split on line, then on sentence, then flatten.
		data = data.toString().trim().split("\n").map(function(x) {
			return x.split(/[\.!?;]/g);
		}).reduce(function(a, b) {
			return a.concat(b);
		}, []);

		// Polly want a dataset?
		var parrot = new markov();
		parrot.addStates(data);
		parrot.train()

		var result = parrot.generateRandom() + ". "
						+ parrot.generateRandom() + ". "
						+ parrot.generateRandom() + ".";
		
		client.sendMessage({
			to: channelID,
			message: result
		});
	});

}

module.exports = mimic;
