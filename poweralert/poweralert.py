# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from schemas import Schemas
from db import users, teams
from poweralert import responses


# ---------------------------------------------------------------------------- #
# --- Discord Configuration -------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
user_db = users.UsersDB()
teams_db = teams.TeamsDB()
schemas = Schemas()
bot = commands.Bot(
    command_prefix='!',
    intents=discord.Intents(value=19327560704).all(),
    help_command=None
) 
TOKEN = os.getenv('TOKEN')
alert = '\n⚡ PowerAlert ⚡\n'
response = responses.Responses()


# ---------------------------------------------------------------------------- #
# --- Discord Events --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def get_user_id(ctx) -> str:
    return f"{ctx.author.name}#{ctx.author.discriminator}"


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")


# ---------------------------------------------------------------------------- #
# --- Discord Commands ------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


@bot.command()
async def hello(ctx):
    """
    Greets the user.
    """
    user_id = get_user_id(ctx)
    logging.info(f"Command executed: {ctx.message.content} - {user_id}")
    await ctx.send(f"{alert}Hi, you can use !help for a list of commands.")


@bot.command()
async def help(ctx):
    """
    Displays all commands.
    """
    user_id = get_user_id(ctx)
    logging.info(f"Command executed: {ctx.message.content} - {user_id}")
    embed = discord.Embed(title="Help", description="List of available commands:", color=0x00ff00)
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def status(ctx):
    """
    Displays national loadshedding status.
    """
    user_id = get_user_id(ctx)
    logging.info(f"Command executed: {ctx.message.content} - {user_id}")
    message = await response.status()
    await ctx.send(message)


@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = error.retry_after
        await ctx.send(f'This command is on cooldown. Please try again in {remaining_time:.2f} seconds.')


@bot.command()
async def list_members(ctx):
    """
    List all members in the server.
    """
    user_id = get_user_id(ctx)
    logging.info(f"Command executed: {ctx.message.content} - {user_id}")
    guild = ctx.guild
    members = guild.members
    member_list = f'{alert}List of members:\n'
    for member in members:
        member_list += f"{member.name}:\t{member}\n"
    await ctx.send(member_list)


@bot.command()
async def create_team(ctx, name, *new_members):
    """
    Creates a team with members from the server.
    eg. !create_team [team_name] (member1#0000) (member2#0000) ...
    """
    user_id = get_user_id(ctx)
    logging.info(f"Command executed: {ctx.message.content} - {user_id}")
    guild = ctx.guild
    member_list = []

    # Check that you don't add members to a team if they are not in the server.
    for member in guild.members:
        member_list.append(f"{member.name}#{member.discriminator}")
    for member in new_members:
        if member not in member_list:
            await ctx.send(f"{alert}{member} is not in the server!") 
            return
    
    # Add the team with members to a database.
    team = schemas.CreateTeam(name=name, members=list(new_members))
    code, message = teams_db.create_team(team)

    # Respond to discord
    if code != 200:
        await ctx.send(message) 
        return

    response = f"{alert}Created new team: {name}\n"
    for member in new_members:
        response += f"\t - {member}"
    await ctx.send(response) 


def run_bot():
    bot.run(TOKEN)