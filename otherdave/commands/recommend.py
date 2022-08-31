import json
import pickledb
import random
from discord import activity, Embed
from otherdave.util import constants

adjectives = json.load(open("./data/madlib/adjectives.json"))

#   recommendations:
#       music:
#           track_id: 
#               <track properties>
#               listeners: 
#                   {user_id, listens}
#       games:
#           <tbd>
recs = pickledb.load("./data/recommendations.db", True)
if (not recs.get("music")):
    recs.dcreate("music")
if (not recs.get("games")):
    recs.dcreate("games")


def playlist(user, song):
    if (not isinstance(song, activity.Spotify)):
        return
    
    if (not recs.dexists("music", song.track_id)):
        recs.dadd(
            "music", 
            (
                song.track_id, 
                { 
                    "title": song.title, 
                    "album": song.album, 
                    "artist": song.artist, 
                    "trackId": song.track_id, 
                    "trackUrl": song.track_url, 
                    "albumCover": song.album_cover_url,
                    "listeners": {}
                }
            ))

    track = recs.dget("music", song.track_id)

    if (user.mention in track["listeners"]):
        track["listeners"][user.mention] += 1
    else:
        track["listeners"][user.mention] = 1

    recs.dump()

def wishlist(user, game):
    if (not isinstance(game, activity.Game)):
        return

def recommend(kind = "-music"):
    if (not (kind in ["-music", "-games"])):
        return Embed(description="I *recommend* you read the usage statement for this command.")
    
    if (kind == "-music"):
        track = recs.dget("music", random.choice(list(recs.dkeys("music"))))
        trackListener = random.choice(list(track["listeners"]))

        embed = Embed(colour=constants.spotifyColor, url=track["trackUrl"], title=track["artist"])
        embed.set_thumbnail(url = track["albumCover"])
        embed.description = constants.musicTemplate.format(
            listener = trackListener,
            title = track["title"],
            trackUrl = track["trackUrl"],
            album = track["album"],
            artist = track["artist"],
            listens = track["listeners"][trackListener],
            adverb = random.choice(adjectives["adverbs"]),
            description = random.choice(adjectives["adjectives"])
        )

        return embed

    if (kind == "-games"):
        return Embed(description="I *recommend* you wait until Isaac finishes writing this bit.")
