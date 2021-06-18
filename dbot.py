#!/usr/bin/env python3

import configparser
import discord
import os
import sys


USER_INI = os.path.abspath(os.path.expanduser('~/.dbot'))

config = configparser.ConfigParser(allow_no_value=True)
config.read(USER_INI)

BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
BOT_USER = config['DEFAULT']['BOT_USER']


def discordPost(toChannel, msg):
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as {0.user}'.format(client))
        channel = discord.utils.get(client.get_all_channels(), name=toChannel)
        if channel:
            await channel.send(msg)
            print("Posted to %s, the message: %s" % (toChannel, msg))
        await client.close()

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    assert len(sys.argv) == 3 and "Need channelName and message"
    toChannel = sys.argv[1]
    msg = sys.argv[2]
    discordPost(toChannel, msg)
