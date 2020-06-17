import pickledb
import yaml
from collections import deque

with open("./conf.yaml", encoding="utf-8") as conf:
    config = yaml.load(conf, Loader=yaml.FullLoader)

memCache = deque(maxlen=config["cache_length"])

async def remember(client, message, args):
    return

async def forget(client, message, args):
    return