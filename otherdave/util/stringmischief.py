# Some helpers for stringMischief down below
def _byteWiseAdd(sthing: str, ithing: int) -> bytes:
    sbytes = sthing.encode("utf-8")
    ibytes = ithing.to_bytes(max(len(sbytes), (ithing.bit_length() + 7) // 8), "big", signed=True)
    if (len(sbytes) < len(ibytes)):
        padbytes = (0).to_bytes((len(ibytes)-len(sbytes)), "big", signed=True)
        sbytes = padbytes + sbytes
    return bytes(list(map(lambda x, y: min(x + y, 255), sbytes, ibytes)))

def _weirdIntAddAndReByte(sthing: str, ithing: int) -> bytes:
    sVal = sum(sthing.encode("utf-8")) + ithing
    return sVal.to_bytes((sVal.bit_length() + 7) // 8, "big")

def _dodgeControlBytes(byteVal: bytes) -> int:
    bint = max(int.from_bytes(byteVal, "big", signed=True), 36)
    if 127 <= bint <= 160:
        return 161
    return bint

# A few insane ways to add an int to a string
stringMischief = [
    # (STR) Simple string concat
    lambda sthing, ithing: str(sthing) + str(ithing),
    # (INT) Sum the string bytes and add the int
    lambda sthing, ithing: sum(sthing.encode("utf-8")) + ithing,
    # (INT) Bytewise addition   
    lambda sthing, ithing: int.from_bytes(_byteWiseAdd(sthing, ithing), "big", signed=True), 
    # (STR) Bytewise addition
    lambda sthing, ithing: "".join(list(map(lambda x: chr(_dodgeControlBytes(x)), _byteWiseAdd(sthing, ithing)))),
    # (STR) Uhhhhhh, don't ask me about this next one
    lambda sthing, ithing: "".join(list(map(lambda x: chr(_dodgeControlBytes(x)), _weirdIntAddAndReByte(sthing, ithing))))
]