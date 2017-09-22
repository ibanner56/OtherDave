"use strict";

var Discord = require("discord.io");
var fs = require('fs');
var logger = require("winston");

var lib = {};

lib.comic = require("./lib/comic.js");
lib.dave = async function(logger, client, user, userID, channelID, args) { 
				client.sendMessage({
					to: channelID,
					message: "OtherDave is not David."
				}); 
		   };
lib.drunkdraw = require("./lib/drunkdraw.js");
lib.haiku = require("./lib/haiku.js");
lib.mimic = require("./lib/mimic.js");
lib.pedant = require("./lib/pedant.js");
lib.respect = require("./lib/respect.js");

var auth = require("./data/auth.json");
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(logger.transports.Console, {
    colorize: true
});
logger.level = "debug";
// Initialize Discord Bot
var client = new Discord.Client({
    token: auth.token,
    autorun: true
});
client.on("ready", function (evt) {
    logger.info("Connected");
    logger.info("Logged in as: ");
    logger.info(client.username + " - (" + client.id + ")");
});
client.on("message", function (user, userID, channelID, message, evt) {
	// OtherDave shouldn't talk to himself.
	if(userID == client.id) {
		return;
	}
	
	if (message.substring(0, 1) == "!") {
		var args = message.trim().substring(1).split(" ");
        var cmd = args[0];

        args = args.splice(1);

		if(cmd in lib) {
			lib[cmd](logger, client, user, userID, channelID, args)
				.catch(function() { });
		} else {
			client.sendMessage({
				to: channelID,
				message: "I'm sorry Dave, I'm afraid I can't do that."
			});
		}	
    } else if(message.indexOf("<@" + client.id + ">") == 0) {
		client.sendMessage({
			to: channelID,
			message: "Hey, you talkin to me?"
		});
	}
	else {
		lib.pedant(logger, client, user, userID, channelID, message)
			.catch(function() {});
		lib.haiku(logger, client, user, userID, channelID, message)
			.catch(function() {});

		// OtherDave is always listening...
		fs.appendFile("./data/markov/" + userID + ".txt", message + "\n", function(error) {
			if(error) {
				logger.error(error);
			}
		});
	}
});
