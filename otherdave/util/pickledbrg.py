import pickledb
import re

pickledb = pickledb

# Extend lget to handle regex values
def lgetrg(self, key: str, value: str) -> str:
    if (not self.exists(key)):
        return None

    items = self.lgetall(key)

    for item in items:
        if (re.match((value), item)):
            return item

    return None

def lexistsrg(self, key: str, value: str) -> bool:
    return lgetrg(self, key, value) != None

# set back the extension methods
pickledb.PickleDB.lgetrg = lgetrg
pickledb.PickleDB.lexistsrg = lexistsrg