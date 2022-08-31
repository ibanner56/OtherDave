# Some helpers for stringMischief down below
def _byteWiseAdd(sthing, ithing):
    sbytes = sthing.encode("utf-8")
    ibytes = ithing.to_bytes(len(sbytes), "big")
    return bytes(list(map(lambda x, y: min(x + y, 255), sbytes, ibytes)))

def _weirdIntAddAndReByte(sthing, ithing):
    sVal = sum(sthing.encode("utf-8")) + ithing
    return sVal.to_bytes((sVal.bit_length() + 7) // 8, "big")

def _dodgeControlBytes(byteVal):
    byteVal = max(byteVal, 36)
    if 127 <= byteVal <= 160:
        return 161
    return byteVal

# A few insane ways to add an int to a string
stringMischief = [
    lambda sthing, ithing: str(sthing) + str(ithing),                           # (STR) Simple string concat
    lambda sthing, ithing: str(_byteWiseAdd(sthing, ithing), "utf-8"),          # (STR) Bytewise addition
    lambda sthing, ithing: int.from_bytes(_byteWiseAdd(sthing, ithing), "big"), # (INT) Bytewise addition
    lambda sthing, ithing: sum(sthing.encode("utf-8")) + ithing,                # (INT) Sum the string bytes and add the int
                                                                                # (STR) Uhhhhhh, don't ask me about this next one
    lambda sthing, ithing: "".join(list(map(lambda x: chr(_dodgeControlBytes(x)), _weirdIntAddAndReByte(sthing, ithing))))
]