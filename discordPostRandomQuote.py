#!/usr/bin/env python3
"""Post a random "Quote of the Day" to a Discord channel.

Reads bot credentials and the target channel from the INI file ``~/.dbot``
(section ``[DEFAULT]``), picks a random quote from ``quotes.tsv`` in this
script's directory, and posts it to the configured channel, then exits.

Expected ``~/.dbot`` keys:
    BOT_TOKEN     - Discord bot token used to authenticate.
    BOT_USER      - Bot user name (unused here; kept for config consistency).
    CHANNEL_NAME  - Name of the channel to post the quote to.

Intended to be run on a schedule (e.g. from cron) as a one-shot command.
"""

import configparser
import csv
import os
import random
import socket

import discord

# INI file holding bot credentials and channel configuration.
USER_INI = os.path.abspath(os.path.expanduser('~/.dbot'))

config = configparser.ConfigParser(allow_no_value=True)
config.read(USER_INI)

BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
BOT_USER = config['DEFAULT']['BOT_USER']
CHANNEL_NAME = config['DEFAULT']['CHANNEL_NAME']

# Tab-separated quotes file living alongside this script. First column is the
# quote text; a header row is skipped when reading.
QUOTES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'quotes.tsv')


def getRandomQuote():
    """Return the text of a random quote from QUOTES_FILE.

    The file is tab-separated with a header row that is skipped. Only the
    first column (the quote text) is used. The chosen quote is also printed
    to stdout for logging.
    """
    with open(QUOTES_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)  # skip header
        rows = list(csv_reader)

    quote = random.choice(rows)[0]
    print(quote)
    return quote


def discordPost():
    """Post a random quote to the configured Discord channel, then exit.

    Connects with the bot token, waits for the ready event, sends the quote
    to CHANNEL_NAME if that channel is found, and closes the connection.

    The posting machine's hostname is appended to the message so that
    duplicate posts (e.g. the same cron job running on more than one machine)
    can be traced back to the machine that sent them.
    """
    # socket.gethostname() identifies which machine posted this quote.
    hostname = socket.gethostname()
    msg = "**Quote of the Day:** " + getRandomQuote()
    msg += "\n_(posted by " + hostname + ")_"

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = discord.utils.get(
            client.get_all_channels(), name=CHANNEL_NAME)
        if channel:
            await channel.send(msg)
        else:
            print("Warning: channel '" + CHANNEL_NAME + "' not found; "
                  "nothing posted")
        await client.close()

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    discordPost()
