import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

teams_dict = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()   
async def openTeam(ctx):
    await ctx.send(f"Wie soll das Team heißen?")

    def check(msg):
        return msg.author == ctx.author

    msg = await bot.wait_for("message", check=check)
    team_name = msg.content

    await ctx.guild.create_voice_channel(team_name)
    
    teams_dict.update({team_name: [msg.author.name]})
    print(teams_dict)
    
    await ctx.send(f"Das Team {team_name} wurde erstellt.")
    
    channel = discord.utils.find(lambda x: x.name == team_name, ctx.guild.channels)
    creator = msg.author

    # user muss mit voice verbunden sein um moved werden zu können
    await creator.move_to(channel)

@bot.command()
async def joinTeam(ctx):
    ctx.send(f"Welchen Team möchtest du beitreten?")
    
    def check(msg):
        return msg.author == ctx.author

    msg = await bot.wait_for("message", check=check)
    team_name = msg.content

    channel = discord.utils.find(lambda x: x.name == team_name, ctx.guild.channels)
    creator = msg.author
    
    # TODO versuchen ob das so funktioniert
    if len(teams_dict[team_name]) < 4:
        teams_dict.update({team_name: [msg.author.name]})
        await creator.move_to(channel)
        await ctx.send(f"Du bist dem dem Team {team_name} beigetreten")
    else:
        await ctx.send("Das Team ist bereits voll")
    

@bot.command()
async def leaveTeam(ctx):
    await ctx.send(f"Welches Team möchtest du verlassen?")
    
    def check(msg):
        return msg.author == ctx.author

    msg = await bot.wait_for("message", check=check)
    team_name = msg.content

    member = msg.author.name.split("#", 1)
    member_list = teams_dict[team_name]
    for i in member_list:
        if member[0] == i:
            member_list.remove(i)
    
    teams_dict.update({team_name: member_list})

    await ctx.send("Du hast das Team verlassen")

    if len(teams_dict[team_name]) < 1:
        teams_dict.pop(team_name)
        await ctx.send("Das Team wurde geschlossen")

@bot.command()
async def teams(ctx):
#    embed = discord.Embed(title="Alle Teams")
#    for t in teams_dict.keys():
#        embed.add_field(name=t)
#        for m in teams_dict[t]:
#            embed.add_field(value=m)
#
#    await ctx.send(embed=embed)

    for t in teams_dict.keys():
        await ctx.send(f"***{t}***")
        for m in teams_dict[t]:
            await ctx.send(m)
        await ctx.send("------------------")

if __name__ == "__main__":
    bot.run(TOKEN)
