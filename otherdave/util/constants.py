from discord import Colour
from otherdave.util import config

inventoryKey = "inventory"
daveBucksKey = "davebucks"

# TODO: It would be neat if there could be a few different madlibs for these responses.
# TODO: Or a better way to set all these than a monolith of constants

# Give response strings
emptyBag = "Aw heck, {whos} all out of stuff."
inventoryPreface = "Well heck, {whove} got a whole bunch of stuff. Right now {whos} carrying:"
unknownThing = "I don't have **{thing}**, give them one yourself."
giftMessage = "Here, {target}, have **{thing}**."
knownThing = "I've already got **{thing}**!"
takeMessage = "Here, have **{thing}**."
thanksMessage = config.selftag + " is now carrying **{thing}**."
thanksfulMessage = config.selftag + " dropped **{oldThing}** and is now carrying **{newThing}**."
foundMessage = "Hey, I found **{thing}**!"
foundfulMessage = "Hey, I found **{newThing}**! Guess I don't need **{oldThing}** any more."
userfulMessage = "..\n\t*...it looks like you've dropped **{thing}** - I hope it wasn't important.*"
greedyMessage = "Noooooooo I only just got that! Get your own, you selfish gremlin."
noBucksMessage = "Hey, you're not <@" + config.daveid + "> <:lwys_todd_eyeburn:912451671181893632>\n\nGet your hands off my :sparkles:DaveBucks:sparkles:, you *capitalist swine*!"
odBucksMessage = "No thanks, dad, all I need is your approval."
daveDaveBucksMessage = "Isn't that a bit, uhhhhh, masturbatory?"
daveWalletMessage = "Wallet? Buddy you're the **bank**."
decimalMessage = "Whoa, you think I'm minting coinage here?"
daveBucksResultMessage = "Alriiiight, {target} now has {daveBucks} DaveBucks! Way to goooo!"
walletMessage = "Well heck, you've got {daveBucks} DaveBucks! Livin' *large*, buddy!"
dropMessage = "*It looks like {who} dropped {whose} **{thing}** - I hope it wasn't important...*"
noDropMessage = "Uhhh, {who} can't drop **{thing}**, {who} don't have one..."
emptyUseMessage = "But {whos} not carrying anything!"
noUseMessage = "{who} can't use **{thing}**, silly, {who} don't have one."
useUsage = "Maybe try using `!help use` first, huh buddy?"

# Haiku response strings
badKeywords = "*The words that you seek,*\n*I simply don't remember.*\n*Did you spell them right?*"
correctionSuccess = "*I've taken your word*\n*that this word was not quite right,*\n*but now it should be.*"
correctionFailed = "*Corrections require*\n*a word and a whole number*\n*What'chu doin', fool?*"
emptyBuffer = "*I don't understand -*\n*we haven't said anything.*\n*Try again later.*"
emptyMemory = "*I don't remember*\n*any of your rad poems.*\n*Make one up instead.*"
forgetSuccess = "*Like fading sunset,*\n*those tired words now fade away.*\n*Eh...they weren't great.*"
savedHaiku = "*Alright then, sounds good,*\n*I'll keep that one for later.*\n*Refrigerator.*"
unknownCritique = "*What you're asking for -*\n*I don't know how to do it.*\n*So piss off, nerd! Yeah!*"

# Ignore and Triggers response strings
ignoreUsage = "Sorry, I don't understand. The correct usage is '!ignore <-me | @user> [minutes]'."
dmsUsage = "Sorry, I dom't understand. The correct usage is '!dms <-enable | -disable>'."
pedantUsage = "*Actually*, the correct usage is '!pedant -me | -stop'."

# Memory response strings
allQuotes = "_all"
badKeywords = "I don't remember saying that."
emptyBuffer = "I haven't said anything yet."
emptyMemory = "Do I even know you people?"
forgetSuccess = "Got it, I'll forget you said that."
forgetYou = "Dude, I *always* forget what you people say."
invalidArgs = "I need a user and some keywords to do that."
notFound = "I don't remember anything they've said!"
saveFailed = "Sorry, I don't remember that."
saveSuccessful = "Got it, I'll save that for later."

# Jabber response strings and resources
notFound = "Buddy, I think you need !help."
joy = ["va-va-voom", "wheee", "whoopee", "woohoo", "yay", "yippee", "yowza"]
version = "OtherDave is running version " + str(config.version)

# Mimic response strings and resources
haikuMakeFailed = "*It seems that today*\n*this request that you have made*\n*is simply too hard.*"
incorrectArgs = "The haha to arguments sorry, for correct not are command that <@ACCIDENTAL_USER_TAG>."
lwysFailed = "Stage: Everyone stares at you, wondering what you're trying to do."
makeFailed = "hahaha Oof owie Heck, guess I don't know you well enough to do that."
lwysCast = ["fixit", "hattie", "oldie", "sophie", "todd", "tomo"]

# Recommend response strings and resources
spotifyColor = Colour(1947988)
musicTemplate = "{listener} has listened to ::\n[{title}]({trackUrl}) on {album} by {artist}\n...{listens} time(s)! It must be {adverb} {description}!"

# Other random constants
tooMuchRespect = "Easy buddy, I can only respect so much at once."