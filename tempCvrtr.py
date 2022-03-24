import disnake
from token import token
from disnake.ext import commands


client = commands.Bot(command_prefix="b|", test_guilds=[951923779859271711], intents=disnake.Intents.default())

client.run(token)