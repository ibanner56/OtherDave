"use strict";

const dlog = require("./dlog.js");
const util = require('util');
const exec = util.promisify(require('child_process').exec);

async function update(logger, client, user) {
    logger.info("Update - user: " + user);
    dlog(client, "Updating to latest OtherDave.")

    try {
        await exec("cd ~/OtherDave | git pull | forever restart 0");
        dlog(client, "Update successful.");
    } catch (err) {
        dlog(client, "And error occurred during update: " + err);
    };
}

module.exports = update;
