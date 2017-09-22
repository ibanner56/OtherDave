"use strict";

var jsdom = require("jsdom");
var { JSDOM } = jsdom;
var mergeImg = require("merge-img");
var randy = require("randy");
var request = require("request");
var _ = require("lodash");

var hopdude_generator = "http://mercworks.net/hopdude_generator/";

function getPanel(logger, panelID, callback) {
	// Parse out Dave's apache directory listing to get the panel options.
	request(hopdude_generator + panelID, function(error, response, body) {
		if(error) {
			logger.error(error);
			return;
		}

		var dom = new JSDOM(body);
		var doc = dom.window.document;
		var listing = doc.getElementsByTagName("ul")[0];
		var entries = Array.from(listing.children);

		// Grab random <li> tag
		var entry = randy.choice(entries.splice(1));
		
		// Crack open inner <a> tag
		var suffix = entry.children[0].innerHTML.trim();
		var imgUrl = hopdude_generator + panelID + suffix;

		request({url: imgUrl, encoding: null}, function(error, response, body) {
			if(error) {
				logger.error(error);
				return;
			}

			callback(body);
		});
	});
}

async function comic(logger, client, user, userID, channelID, args) {
	var panel1 = null;
	var panel2 = null;
	var panel3 = null;
	var finished = _.after(3, doMerge);

	// Callback hell
	getPanel(logger, "panel01/", function(image) {
		panel1 = image;
		finished();
	});
	getPanel(logger, "panel02/", function(image) {
		panel2 = image;
		finished();
	});
	getPanel(logger, "panel03/", function(image) {
		panel3 = image;
		finished();
	});

	function doMerge() {
		mergeImg([panel1, panel2, panel3])
			.then( function(img) {
				img.getBuffer(img.getMIME(), function(error, buffer) {
					if(error) {
						logger.error(error)
						return;
					}
					
					client.uploadFile({
						to: channelID,
						file: buffer,
						filename: "comic.png",
						// message: "<@359850424766824458>, make me beautiful!",
						message: "Mama Mia!",
						callback: function(error, response) {
							if(error) {
								logger.error(error);
							}
						}
					});
				});
			});
	}
}

module.exports = comic;
