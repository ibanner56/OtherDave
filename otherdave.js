"use strict";

var Discord = require("discord.io");
var logger = require("winston");

var lib = {};

lib.dave = function(logger, client, user, userID, channelID, args) { 
				client.sendMessage({
					to: channelID,
					message: "OtherDave is not David."
				}); 
		   };
lib.drunkdraw = require("./lib/drunkdraw.js");
lib.respect = require("./lib/respect.js");
lib.comic = require("./lib/comic.js");

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
	if (message.substring(0, 1) == "!") {
		client.simulateTyping(channelID);

		var args = message.trim().substring(1).split(" ");
        var cmd = args[0];

        args = args.splice(1);

		if(cmd in lib) {
			lib[cmd](logger, client, user, userID, channelID, args);
		} else {
			client.sendMessage({
				to: channelID,
				message: "I'm sorry Dave, I'm afraid I can't do that."
			});
		}	
    }
});
