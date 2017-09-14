"use strict";

var Discord = require("discord.io");
var logger = require("winston");

var lib = {};

lib.dave = function() { return "OtherDave is not David."; };
lib.drunkdraw = require("./lib/drunkdraw.js");
lib.respect = require("./lib/respect.js");

var auth = require("./data/auth.json");
// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(logger.transports.Console, {
    colorize: true
});
logger.level = "debug";
// Initialize Discord Bot
var bot = new Discord.Client({
    token: auth.token,
    autorun: true
});
bot.on("ready", function (evt) {
    logger.info("Connected");
    logger.info("Logged in as: ");
    logger.info(bot.username + " - (" + bot.id + ")");
});
bot.on("message", function (user, userID, channelID, message, evt) {
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`
    if (message.substring(0, 1) == "!") {
        var args = message.trim().substring(1).split(" ");
        var cmd = args[0];

        args = args.splice(1);

		if(cmd in lib) {
			bot.sendMessage({
				to: channelID,
				message: lib[cmd](logger, user, args)
			});
		} else {
			bot.sendMessage({
				to: channelID,
				message: "I'm sorry Dave, I'm afraid I can't do that."
			});
		}	
    }
});
