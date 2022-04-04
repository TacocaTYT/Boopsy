import disnake
from disnake.ext import commands
from my_token import my_token
from random_word import RandomWords
rw = RandomWords()
from PyDictionary import PyDictionary
dictionary = PyDictionary()
import logging
import asyncio
gameIDdict = {
  1:"shitty scrabble",
  2:"hangman"
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
client.guessedLetters = {}


@client.event
async def on_ready():
  print(f'Ready to rumble.')


@client.slash_command(
  name="init__util_gm",
  description="Initialization utility that also assigns the gamemaster role to the indicated user"
)
async def initutil(ctx, user: disnake.Member = None):
  user = user or ctx.author
  if disnake.utils.get(ctx.author.roles,name="Gamemaster") is not None or ctx.author.id == ctx.guild.owner_id:
    role = disnake.utils.get(ctx.guild.roles, name="Gamemaster")
    if role is None:
      role = await ctx.guild.create_role(name="Gamemaster",reason="init__util_gm/created_role")
    await user.add_roles(role,reason="init__util_gm/assigned_role")
    await ctx.send(content=f"<@{user.id}> has been given the {role} role.", delete_after=5.0)


@client.slash_command(
  name="init__util_gm",
  description="Initialization utility that also assigns the gamemaster role to the indicated user"
)
async def initutil(ctx, user: disnake.Member = None):
  user = user or ctx.author
  if disnake.utils.get(ctx.author.roles,name="Gamemaster") is not None or ctx.author.id == ctx.guild.owner_id and client.channelGame[ctx.channel.id] == 2:
    await ctx.send(dictionary.meaning(client.leadWord[ctx.channel.id]))
  else:
    await ctx.send("You are not a gamemaster or there is not a hangman game in this channel.", ephemeral=True)


@client.slash_command(
  name="start_game",
  description="Start a game from the list."
)
async def startGame(ctx, gameid: int = 1):
  client.channelGame[ctx.channel.id] = gameid
  if disnake.utils.get(ctx.author.roles,name="Gamemaster") is not None:
    try:
      if gameid == 1:
        client.leadWord[ctx.channel.id] = ""
        client.leadWordPoints[ctx.channel.id] = 0
        client.leadPlayer[ctx.channel.id] = "<@885311386207526932>"
        embedVar = disnake.Embed(title=f"The game has begun!", description="", color=0x00ff00)
        embedVar.add_field(name="Score to Beat:", value=client.leadWord[ctx.channel.id] + " worth " + str(client.leadWordPoints[ctx.channel.id]) + " points from " + str(client.leadPlayer[ctx.channel.id]), inline=False)
        embedVar.add_field(name="Next Player: ", value=f"<@{client.players[ctx.channel.id][0]}>", inline=False)
      
      elif gameid == 2:
        client.leadWord[ctx.channel.id] = str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower()
        while " " in client.leadWord[ctx.channel.id] or "_" in client.leadWord[ctx.channel.id]:
          client.leadWord[ctx.channel.id] = str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower()
        print(client.leadWord[ctx.channel.id])
        client.leadWordPoints[ctx.channel.id] = ""
        client.guessedLetters[ctx.channel.id] = ["-"]
        for i in client.leadWord[ctx.channel.id]:
          if i in client.guessedLetters[ctx.channel.id]:
            client.leadWordPoints[ctx.channel.id] += f"{i}"
          else:
            client.leadWordPoints[ctx.channel.id] += "[]"
        embedVar = disnake.Embed(title=f"Hangman", description=f"{client.leadWordPoints[ctx.channel.id]}", color=0x00ff00)
        embedVar.add_field(name="Next Player: ", value=f'<@{client.players[ctx.channel.id][0]}>', inline=False)
        embedVar.add_field(name=f"Guessed Letters", value=f"{client.guessedLetters[ctx.channel.id]}")
      
      await ctx.send(embed=embedVar)
      client.currentEmbed[ctx.channel.id] = await ctx.original_message()
      client.currentGameChannel = ctx.channel.id

      while client.players[ctx.channel.id]:
        try:
          isPlayer = lambda message : message.author.id == client.players[message.channel.id][0]
          message = await client.wait_for("message", check = isPlayer, timeout = 5)
          if message.channel.id in client.channelGame:
            if client.channelGame[message.channel.id] == 1 and len(message.content) <= 45 and " " not in message.content: #Bad Scrabble
              client.remainingCharacters = len(message.content)
              while client.remainingCharacters > 0:
                  for i in message.content:
                      for key in pointDict:
                          if i == key:
                              client.points += pointDict[key]
                              client.remainingCharacters -= 1

              await message.delete()
              #If highscore
              if client.points > client.leadWordPoints[message.channel.id]:
                  embedVar = disnake.Embed(title=f"{message.author}'s turn!", description=f"{message.author}'s word was {message.content}, worth {client.points} points", color=0x00ff00)
                  embedVar.add_field(name="Score to Beat:", value=client.leadWord[message.channel.id] + " worth " + str(client.leadWordPoints[message.channel.id]) + " points from " + str(client.leadPlayer[message.channel.id]), inline=False)
                  client.players[message.channel.id].insert(len(client.players[message.channel.id]), client.players[message.channel.id].pop(0))
                  embedVar.add_field(name="Next Player: ", value=f'<@{client.players[message.channel.id][0]}>', inline=False)
                  client.leadPlayer[message.channel.id] = message.author
                  client.leadWord[message.channel.id] = message.content
                  client.leadWordPoints[message.channel.id] = client.points
                  await client.currentEmbed[message.channel.id].edit(embed=embedVar)
              #If not highscore
              else:
                  embedVar = disnake.Embed(title=f"{message.author}'s turn!", description=f"{message.author}'s word was {message.content}, worth {client.points} points", color=0x00ff00)
                  embedVar.add_field(name="Score to Beat:", value=client.leadWord[message.channel.id] + " worth " + str(client.leadWordPoints[message.channel.id]) + " points from " + str(client.leadPlayer[message.channel.id]), inline=False)
                  client.players[message.channel.id].insert(len(client.players[message.channel.id]), client.players[message.channel.id].pop(0))
                  embedVar.add_field(name="Next Player: ", value=f'<@{client.players[message.channel.id][0]}>', inline=False)
                  await client.currentEmbed[message.channel.id].edit(embed=embedVar)
              client.points = 0

            if client.channelGame[message.channel.id] == 2: #Hangman
                  client.players[message.channel.id].insert(len(client.players[message.channel.id]), client.players[message.channel.id].pop(0))
                  if str(message.content).lower() == client.leadWord[message.channel.id]:
                      embedVar = disnake.Embed(title=f"{message.author} successfuly guessed the word, {client.leadWord[message.channel.id]}")
                      await client.currentEmbed[message.channel.id].edit(embed=embedVar)
                      client.channelGame[message.channel.id] = 0
                      client.players[message.channel.id] = []
                  elif len(str(message.content)) == 1 and str(message.content).isalpha() and str(message.content).lower() not in client.guessedLetters[message.channel.id]:
                      client.leadWordPoints[message.channel.id] = ""
                      client.guessedLetters[message.channel.id] += str(message.content).lower()
                      for i in client.leadWord[message.channel.id]:
                          if i in client.guessedLetters[message.channel.id]:
                              client.leadWordPoints[message.channel.id] += f"{i}"
                      else:
                          client.leadWordPoints[message.channel.id] += "[]"
                      embedVar = disnake.Embed(title=f"Hangman", description=f"{client.leadWordPoints[message.channel.id]}", color=0x00ff00)
                      embedVar.add_field(name="Next Player: ", value=f'<@{client.players[message.channel.id][0]}>', inline=False)
                      embedVar.add_field(name=f"Guessed Letters", value=f"{client.guessedLetters[message.channel.id]}")
                  else:
                      embedVar = disnake.Embed(title=f"Hangman", description=f"{client.leadWordPoints[message.channel.id]}", color=0x00ff00)
                      embedVar.add_field(name="Next Player: ", value=f'<@{client.players[message.channel.id][0]}>', inline=False)
                      embedVar.add_field(name=f"Guessed Letters", value=f"{client.guessedLetters[message.channel.id]}")
                  await message.delete()
                  await client.currentEmbed[message.channel.id].edit(embed=embedVar)
        except asyncio.TimeoutError:
          await ctx.send(f"<@{client.players[ctx.channel.id][0]}> has been removed from the Queue", delete_after = 5)
          client.players[ctx.channel.id].pop(0)
      if client.channelGame[ctx.channel.id]:
        embedVar = disnake.Embed(title=f"This game of {gameIDdict[client.channelGame[ctx.channel.id]]} has ended.")
        await client.currentEmbed[ctx.channel.id].edit(embed=embedVar)
        client.channelGame[ctx.channel.id] = 0

    except Exception as e:
      print(e)
      await ctx.send("Can't start a game with 0 players! Use ``/join_game``", ephemeral=True)
      client.channelGame[ctx.channel.id] = 0
  else:
    await ctx.send(content="You are not a gamemaster", ephemeral=True)


@client.slash_command(
  name="game_list",
  description="List the available game IDs"
)
async def gameIDlist(ctx):
  await ctx.send(content=f'```py{gameIDdict}```', delete_after=5)


@client.slash_command(
  name="end_game",
  description="End the current game"
)
async def endGame(ctx):
  if disnake.utils.get(ctx.author.roles,name="Gamemaster") is not None:
    try:
      client.channelGame[ctx.channel.id] = 0
      client.players[ctx.channel.id] = []
      await ctx.send(f'Game Ended')
    except:
      await ctx.send(content="An unknown error occured", ephemeral=True)
  else:
    await ctx.send(content="You are not a gamemaster", ephemeral=True)


@client.slash_command(
  name="join_game",
  description="Join the game being played in this channel"
)
async def joinGame(ctx):
  if ctx.channel.id not in client.players:
    client.players[ctx.channel.id] = []
  if ctx.author.id in client.players[ctx.channel.id]:
    await ctx.send(f'<@{ctx.author.id}>, you are already in the game, no need to join twice.', ephemeral=True)
  else:
    await ctx.send(f'<@{ctx.author.id}> has joined the round!', delete_after=3.0)
    client.players[ctx.channel.id].append(ctx.author.id)

client.run(my_token)