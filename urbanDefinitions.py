#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Delta Kapp
Date: 2022-03-30

Urban Dictionary Discord Bot

Bot requires permission to read and make messages.

HOW TO USE BOT:

'$define xyz' retrieves definition for xyz
    for example: $define fun
    retrieves most popular definition for 'fun'

'$defineN xyz' where N is an integer, retrieves Nth definition for xyz
    for example: $define3 free
    retrieves third most popular definition for 'free'
"""

import json

import discord
import requests

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    """
    attempts to return Urban Dictionary definition for message
    """
    try:
        if message.author == client.user:
            return

        if message.content.startswith("$define"):
            index_string = message.content.split()[0][7:]
            if index_string == "":
                index = 0
            else:
                index = int(index_string) - 1
            word = " ".join(message.content.split()[1:])
            response = requests.get(
                f"http://api.urbandictionary.com/v0/define?term={word}"
            )
            response_list = json.loads(response.text)["list"]
            dictionary_list = sorted(
                response_list, key=lambda d: d["thumbs_up"] - d["thumbs_down"]
            )
            result = f":book: defining ***{word}*** for {message.author.mention}:\n"
            if len(dictionary_list) == 0:
                result += f":pleading_face: No definition found."
                await message.channel.send(result)
                return
            if index > len(dictionary_list):
                index = -1
                result += f":nerd: unfortunately there are only {len(dictionary_list)} definitions. Here is the last one:\n"
            entry = dictionary_list[index]
            result += "> "
            result += (
                entry["definition"]
                .replace("[", "")
                .replace("]", "")
                .replace("\n", "\n> ")
            )
            url = requests.get(entry["permalink"]).url
            result += f"\n<{url}>\n`{entry['thumbs_up']}`:arrow_up:  `{entry['thumbs_down']}`:arrow_down:  by *{entry['author']}*"
            await message.channel.send(result)
            return
    except:
        await message.channel.send("An error occurred.")


client.run("bots-secret-token")
