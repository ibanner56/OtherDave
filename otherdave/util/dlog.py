channelId = "697547257758613656"

async def dlog(client, message):
    logChannel = await client.fetch_channel(channelId)
    await logChannel.send(message)