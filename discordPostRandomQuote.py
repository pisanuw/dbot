#!/usr/bin/env python3

import configparser
import csv
import discord
import os
import random

USER_INI = os.path.abspath(os.path.expanduser('~/.dbot'))

config = configparser.ConfigParser(allow_no_value=True)
config.read(USER_INI)

BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
BOT_USER = config['DEFAULT']['BOT_USER']

QUOTES_FILE = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'quotes.tsv')

# CHANNEL_NAME = 'privateadmin'
CHANNEL_NAME = 'chit-chat'


def getRandomQuote():
    with open(QUOTES_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        lineCount = 0
        lines = []
        # skip header
        next(csv_reader)
        for row in csv_reader:
            lineCount += 1
            lines.append(row)
    num = random.randint(0, len(lines) - 1)
    quote = lines[num][0]
    print(quote)
    return quote


def discordPost():
    msg = getRandomQuote()
    msg = "**Quote of the Day:** " + msg
    client = discord.Client()

    @client.event
    async def on_ready():
        channel = discord.utils.get(
            client.get_all_channels(), name=CHANNEL_NAME)
        if channel:
            await channel.send(msg)
        await client.close()

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    discordPost()
