channelId = "697547257758613656"

def log(client, message):
    logChannel = client.get_channel(channelId)
    logChannel.send(message)