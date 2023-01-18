import discord

channelId = "697547257758613656"

async def dlog(client: discord.Client, message: str) -> None:
    logChannel = await client.fetch_channel(channelId)
    await logChannel.send(message)