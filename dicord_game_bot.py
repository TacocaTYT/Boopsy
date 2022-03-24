import disnake
from disnake.ext import commands
from my_token import my_token
import logging
gameIDdict = {
  "scrabble" : 1,
  "hangman" : 2
}
pointDict = {
  "a" : 1,
  "b" : 3,
  "c" : 3,
  "d" : 2,
  "e" : 1,
  "f" : 4,
  "g" : 2,
  "h" : 4,
  "i" : 1,
  "j" : 8,
  "k" : 5,
  "l" : 1,
  "m" : 3,
  "n" : 1,
  "o" : 1,
  "p" : 3,
  "q" : 10,
  "r" : 1,
  "s" : 1,
  "t" : 1,
  "u" : 1,
  "v" : 4,
  "w" : 4,
  "x" : 8,
  "y" : 4,
  "z" : 10,
  "-" : -1
}

client = commands.Bot(command_prefix="b|", test_guilds=[951923779859271711], intents=disnake.Intents.default())
client.players = {}
client.nextPlayer = "<@885311386207526932>"
client.channelGame = {}
client.remainingCharacters = 0
client.points = 0
client.leadWordPoints = {}
client.leadWord = {}
client.leadPlayer = {}
client.currentEmbed = {}

@client.event
async def on_ready():
  print(f'Ready to rumble.')
@client.slash_command(
  name="start_game",
  description="Start a game from the list."
)
async def startGame(ctx, gameID: int = 1):
  client.leadWord[ctx.channel.id] = ""
  client.leadWordPoints[ctx.channel.id] = 0
  client.channelGame[ctx.channel.id] = gameID
  client.leadPlayer[ctx.channel.id] = "<@885311386207526932>"
  embedVar = disnake.Embed(title=f"The game has begun!", description="", color=0x00ff00)
  embedVar.add_field(name="Score to Beat:", value=client.leadWord[ctx.channel.id] + " worth " + str(client.leadWordPoints[ctx.channel.id]) + " points from " + str(client.leadPlayer[ctx.channel.id]), inline=False)
  embedVar.add_field(name="Next Player: ", value=f"<@{client.players[ctx.channel.id][0]}>", inline=False)
  await ctx.send(embed=embedVar)
  client.currentEmbed[ctx.channel.id] = await ctx.original_message()
  client.currentGameChannel = ctx.channel.id


@client.slash_command(
  name="game_list",
  description="List the available game IDs"
)
async def gameIDlist(ctx):
  await ctx.send(f'```py\n{gameIDdict}```')


@client.slash_command(
  name="join_game",
  description="Join the game being played in this channel"
)
async def joinGame(ctx):
  #await ctx.message.delete()
  if ctx.channel.id not in client.players:
    client.players[ctx.channel.id] = []
  if ctx.author.id in client.players[ctx.channel.id]:
    await ctx.send(f'{ctx.author}, you are already in the game, no need to join twice.')
  else:
    await ctx.send(f'<@{ctx.author.id}> has joined the round!')
    client.players[ctx.channel.id].append(ctx.author.id)


@client.listen()
async def on_message(message):
  try:
    if message.channel.id in client.channelGame.keys():
      if message.author != client.user and message.author.id == client.players[message.channel.id][0]:
        if len(message.content) <= 45 and " " not in message.content:
          client.remainingCharacters = len(message.content)
          while client.remainingCharacters > 0:
            for i in message.content:
              for key in pointDict:
                if i == key:
                  client.points += pointDict[key]
                  client.remainingCharacters -= 1
          await message.delete()
          #await message.channel.send(message.content + " is worth " + str(client.points) + " points")
          if client.points > client.leadWordPoints[message.channel.id]:
            embedVar = disnake.Embed(title=f"{message.author}'s turn!", description=f"{message.author}'s word was {message.content}, worth {client.points} points", color=0x00ff00)
            embedVar.add_field(name="Score to Beat:", value=client.leadWord[message.channel.id] + " worth " + str(client.leadWordPoints[message.channel.id]) + " points from " + str(client.leadPlayer[message.channel.id]), inline=False)
            client.players[message.channel.id].insert(len(client.players[message.channel.id]), client.players[message.channel.id].pop(0))
            embedVar.add_field(name="Next Player: ", value=f'<@{client.players[message.channel.id][0]}>', inline=False)
            client.leadPlayer[message.channel.id] = message.author
            client.leadWord[message.channel.id] = message.content
            client.leadWordPoints[message.channel.id] = client.points
            await client.currentEmbed[message.channel.id].edit(embed=embedVar)
          else:
            embedVar = disnake.Embed(title=f"{message.author}'s turn!", description=f"{message.author}'s word was {message.content}, worth {client.points} points", color=0x00ff00)
            embedVar.add_field(name="Score to Beat:", value=client.leadWord[message.channel.id] + " worth " + str(client.leadWordPoints[message.channel.id]) + " points from " + str(client.leadPlayer[message.channel.id]), inline=False)
            client.players[message.channel.id].insert(len(client.players[message.channel.id]), client.players[message.channel.id].pop(0))
            embedVar.add_field(name="Next Player: ", value=f'<@{client.players[message.channel.id][0]}>', inline=False)
            await client.currentEmbed[message.channel.id].edit(embed=embedVar)
          client.points = 0
  except IndexError:
    print("Index out of range, probably empty still")

client.run(my_token)