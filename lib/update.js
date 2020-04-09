"use strict";

var dlog = require("./dlog.js");
var exec = require("child_process");

async function update(logger, client, user) {
    logger.info("Update - user: " + user);
    dlog(client, "Updating to latest OtherDave.")

    exec("cd ~/OtherDave | git pull | forever restart 0", (err) => {
        if (err) {
            dlog(client, "And error occurred during update: " + err);
            return;
        } 
        else {
            dlog(client, "Update successful.");
        }
    });
}

module.exports = update;
