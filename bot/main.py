import os
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")
@bot.command()   
async def neuesTurnier(ctx):
    await ctx.send(f"Gib dem Turnier einen Namen:")

    def check(msg):
        return msg.author == ctx.author

    msg = await bot.wait_for("message", check=check)
    tournament_name = msg.content

    await ctx.guild.create_voice_channel(tournament_name)

    await ctx.move_member(msg.author, tournament_name)

if __name__ == "__main__":
    bot.run(TOKEN)
