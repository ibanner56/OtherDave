import pickledb
import re

pickledb = pickledb

# Extend lget to handle regex values
def lgetrg(self, key, value):
    if (not self.exists(key)):
        return None

    items = self.lgetall(key)

    for item in items:
        if (re.match((value), item)):
            return item

    return None

def lexistsrg(self, key, value):
    return lgetrg(self, key, value) != None

# set back the extension methods
pickledb.PickleDB.lgetrg = lgetrg
pickledb.PickleDB.lexistsrg = lexistsrg