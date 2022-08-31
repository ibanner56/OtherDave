import yaml

with open("./conf.yaml") as conf:
    loadedConfig = yaml.load(conf, Loader=yaml.BaseLoader)

version = loadedConfig["version"]
description = loadedConfig["description"]

cacheLength = int(loadedConfig["cache_length"])
maxLookback = int(loadedConfig["max_lookback"])
parrotChan = loadedConfig["parrot_channel"]
parrotInterval = loadedConfig["parrot_interval"]
daveid = loadedConfig["dave_id"]
selfid = loadedConfig["self_id"]
selftag = "<@" + selfid + ">"
bagsize = int(loadedConfig["bag_size"])
userbagsize = int(loadedConfig["user_bag_size"])
greedytime = int(loadedConfig["greedy_time"])

drunkdraw = loadedConfig["drunkdraw"]
emotions = loadedConfig["emotions"]
rereactions = loadedConfig["rereactions"]