#!/usr/bin/env python3

import configparser
import csv
import discord
import os
import random
import sys
from discord.utils import get

USER_INI = os.path.abspath(os.path.expanduser('~/.dbot'))

config = configparser.ConfigParser(allow_no_value=True)
config.read(USER_INI)

BOT_TOKEN = config['DEFAULT']['BOT_TOKEN']
BOT_USER = config['DEFAULT']['BOT_USER']
CHANNEL_NAME = config['DEFAULT']['CHANNEL_NAME']
LOG_CHANNEL_NAME = config['DEFAULT']['LOG_CHANNEL_NAME']
GUILD_NAME = config['DEFAULT']['GUILD_NAME']

addRoleName = "member"
removeRoleName = "member_UNVERIFIED"


def getGuild(client):
    for guild in client.guilds:
        if guild.name == GUILD_NAME:
            # print(guild.name, guild.id)
            return guild
    return None


async def removeRoleSingle(user, role):
     if role not in user.roles:
        print(user.name + " does not have role " + role.name + ". Cannot remove")
     else:
         await user.remove_roles(role)
         print(user.name + "'s role removed: " + role.name)

async def addRoleSingle(user, role):
     if role in user.roles:
        print(user.name + " already has role " + role.name + ". Cannot add")
     else:
         await user.add_roles(role)
         print(user.name + "'s role added: " + role.name)         
         
def discordApprove(usernames):
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    approvedMsg = "You have been approved for UWB Pisan. Choose your course channel in #general. https://discord.com/channels/358309182140710912/559516062090002452"
    
    @client.event
    async def on_ready():
        guild = getGuild(client)
        channel = discord.utils.get(client.get_all_channels(), name=LOG_CHANNEL_NAME)
        memberRole = discord.utils.get(guild.roles, name=addRoleName)
        unverifiedRole = discord.utils.get(guild.roles, name=removeRoleName)
        # print(channel, guild, memberRole, unverifiedRole)
        gms = {}
        for m in guild.members:
            gms[m.name + "#" + m.discriminator] = m
        for username in usernames:
            if username not in gms:
                print("Could not find user: " + username)
                continue
            m = gms[username]
            await removeRoleSingle(m, unverifiedRole)
            await addRoleSingle(m, memberRole)
            # await addRoleSingle(m, unverifiedRole)
            await m.send(approvedMsg)
            await channel.send(username + " <@" + str(m.id) +">" + " approved ")
        await client.close()

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: discardApproveUsers.py user#12 [user2#34 user3#45 ...]")
        sys.exit(0)
    discordApprove(sys.argv[1:])
