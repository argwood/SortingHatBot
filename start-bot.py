import discord
import asyncio
import sys, io, os
import logging

import sortinghat

client = discord.Client()

try:
    token = os.environ['TOKEN']
    sorting_channel = os.environ['CHANNEL_ID']
except KeyError:
    print('Pleae provide an appropriate bot token and channel ID to begin. Use: export TOKEN = \'my_token_here\' and export CHANNEL_ID = \'my_channel_id\'.')
    client.close()

sorting_hat = sortinghat.SortingHat(client)

@client.event
async def on_ready():
    print('Waking up the Sorting Hat...')

@client.event
async def on_message(message):
    if sorting_channel in message.channel.id:
        if message.content.lower().startswith('!sort'):
            await sorting_hat.start(message)
        if message.content.lower().startswith('!stop'):
            await sorting_hat.stop(message.channel)
        if message.content.lower().startswith('yes'):
            await sorting_hat.quiz(message)
        if message.content.lower().startswith('!start'):
            await client.send_message(message.channel, 'Type `!sort` to begin to the Sorting Ceremony')

if __name__ == "__main__":

    try:
        client.run(token)
    except:
        client.close()
