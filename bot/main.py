import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

teams = {}

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
    
    channel = discord.utils.find(lambda x: x.name == team_name, ctx.guild.channels)
    creator = msg.author

    teams.update(team_name = [msg.author.name])
    print(teams)

    # user muss mit voice verbunden sein um moved werden zu können
    await creator.move_to(channel)

@bot.command()
async def joinTeam(ctx):
    pass

if __name__ == "__main__":
    bot.run(TOKEN)
