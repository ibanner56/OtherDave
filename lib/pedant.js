"use strict";

var xkcd37 = require("xkcd-37");

/**
* Collection of detections and pedantry
*/
function pedant(logger, client, user, userID, channelID, message) {
	message = message.toLowerCase();

	if(message.includes("-ass")) {
		client.sendMessage({
			to: channelID,
			message: xkcd37(message)
		});
		return;
	}

	if(message.includes("issac") && user == "1076") {		
		client.sendMessage({
			to: channelID,
			message: "Oh, did you mean 'Isaac'?"
		});
	}
}

module.exports = pedant;
