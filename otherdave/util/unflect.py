# Strip the indefinite article from an articled string
def a(word: str) -> str:
    if (word.startswith("a ")):
        return word[2:]
    if (word.startswith("an ")):
        return word[3:]
    # No indefinite article
    return word

# Alias an to a to be cute like inflect
def an(word: str) -> str: return a(word)