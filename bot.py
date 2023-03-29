import json
import os
import asyncio
import discord
import string
import random
from discord.ext import commands

new=discord.Embed(title="新版本V1.02",description="新版本發布了以下功能\n```評價功能```\n修復:\n```N/A```")


with open("config.json", "r", encoding="UTF-8") as file:
    data = json.load(file)
TOKEN = data["token"]

bot = commands.Bot(help_command=None, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"┌──────────┐")
    print(f"│{bot.user} │")
    print(f"│成      功│")
    print(f"│連      線│")
    print(f"│  Discord │")
    print(f"└──────────┘")
    game = discord.Game(f"期待您的加入")
    await bot.change_presence(status=discord.Status.online, activity=game)
    channel = bot.get_channel(1079959287301935114)
    
    
    
@bot.event
async def on_message(message):
    print(f"{message.author} | {message.guild}-{message.channel}-{message.content}")
    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'✅   已加載 {filename}')
        except Exception as error:
            print(f'❎   {filename} 發生錯誤  {error}')


bot.run(TOKEN)