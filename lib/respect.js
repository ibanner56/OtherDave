"use strict";
var execSync = require("child_process").execSync;

function respect(logger, user, message) {
	logger.info("Respect - user: " + user + ", message: " + message);

	var args = message.split(" ").slice(1);
	var target = user;

	if (args.length > 0) {
		target = args[0];
	}

	var compliment = 
		execSync("python ./lib/mad/madlib.py madlib ./lib/mad/data/compliments.dat")
		.toString("utf8").trimRight("\n").toLowerCase();
	return target + ", " + compliment;
}

module.exports = respect; 
