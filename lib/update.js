"use strict";

const dlog = require("./dlog.js");
const util = require('util');
const exec = util.promisify(require('child_process').exec);

function update(logger, client, user) {
    logger.info("Update - user: " + user);
    dlog(client, "Updating to latest OtherDave.")

    return exec("cd ~/OtherDave | git pull | forever restart 0");
}

module.exports = update;
