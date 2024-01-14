import os

import aiohttp
import discord
import datetime as dt
import re
from discord import app_commands
from discord import Interaction
from discord.app_commands.errors import MissingAnyRole
from discord.app_commands.checks import has_any_role

import db


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    @staticmethod
    async def on_message(message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

tree = app_commands.CommandTree(client)


@tree.command(name='add_emoji', description='adds custom emoji', guild=discord.Object(id=435757455595798539))
async def add_emoji(interaction: Interaction, emoji: str, name: str = None):
    try:
        emj_anim, emj_name, emj_id = emoji.strip('<>').split(':')
        print(emj_id)
        emj_format = 'webp' if not emj_anim else 'gif'
        url = f'https://cdn.discordapp.com/emojis/{emj_id}.{emj_format}'
        if not name:
            name = emj_name
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                emoji = await interaction.guild.create_custom_emoji(name=name, image=await resp.read())
    except Exception as e:
        print(f"[ERROR] {e}")
        await interaction.response.send_message("Произошла ошибка!")
    else:
        await interaction.response.send_message(f"Эмодзи {emoji}")


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=435757455595798539))
    print("Ready!")

client.run('MTE5NjA1NzAxMDM4NzU1MDI1OA.GxKiyj.fA9PjE2Q9PKuL35_4E9rH2oboKDgRb1sWDeBNI')
