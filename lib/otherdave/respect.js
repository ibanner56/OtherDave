"use strict";

function respect(logger, user, message) {
	logger.info("Respect - user: " + user + ", message: " + message);

	var args = message.split(" ").slice(1);
	var target = user;

	if (args.length > 0) {
		target = args[0];
	}

	return "";
}
