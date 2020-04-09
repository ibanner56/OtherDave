"use strict";

var log = require("./log.js");
var exec = require("child_process");

async function update(client, ) {
    log(client, "Updating to latest OtherDave.")
    exec("cd ~/OtherDave | git pull | forever restart 0", (err) => {
        if (err) {
            log(client, "And error occurred during update: " + err);
            return;
        } 
        else {
            log(client, "Update successful.");
        }
    });
}

module.exports = update;
