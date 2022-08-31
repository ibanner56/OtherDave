import yaml

with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)

version = config["version"]
description = config["description"]

cacheLength = int(config["cache_length"])
maxLookback = int(config["max_lookback"])
parrotChan = config["parrot_channel"]
parrotInterval = config["parrot_interval"]
daveid = config["dave_id"]
selfid = config["self_id"]
selftag = "<@" + selfid + ">"
bagsize = int(config["bag_size"])
userbagsize = int(config["user_bag_size"])
greedytime = int(config["greedy_time"])

drunkdraw = config["drunkdraw"]
emotions = config["emotions"]
rereactions = config["rereactions"]