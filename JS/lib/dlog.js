"use strict";

var logChannel = "697547257758613656";

async function dlog(client, message) {
	client.sendMessage({
		to: logChannel,
		message: message
    });
}

module.exports = dlog;