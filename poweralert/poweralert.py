# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Tuple
from db import teams, users
from poweralert import responses
from poweralert.logger import logger
from schemas import Schemas

# ---------------------------------------------------------------------------- #
# --- Discord Configuration -------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()
log = logger()
user_db = users.UsersDB()
teams_db = teams.TeamsDB()
schemas = Schemas()
intents = discord.Intents(value=19235045637216).all()
intents.members = True
bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    help_command=None
)
TOKEN = os.getenv('TOKEN')
alert = '\n⚡ PowerAlert ⚡\n'
response = responses.Responses()


# ---------------------------------------------------------------------------- #
# --- Discord Events --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def get_user_id(ctx) -> str:
    """
    Returns the user id in format:
    name#discrimonator

    returns str (username#0000)
    """
    return f"{ctx.author.name}#{ctx.author.discriminator}"

def get_server_details(ctx) -> Tuple[int, str]:
    """
    Returns the server id and name:
    server_id, server_name

    returns Tuple[int, str] (server_id, server_name)
    """
    if ctx.guild is not None:
        return ctx.guild.id, ctx.guild.name
    return None, None


@bot.event
async def on_ready():
    log.on_ready(bot.user.name, bot.user.id)


# ---------------------------------------------------------------------------- #
# --- Discord Commands ------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


    # ------------------------------------------------------------------------ #
    # --- General Commands --------------------------------------------------- #
    # ------------------------------------------------------------------------ #


# !test
@bot.command()
async def test(ctx):
    id, name = get_server_details(ctx)
    print(f"name: {name}, id: {id}")


# !hello
@bot.command()
async def hello(ctx):
    """
    Greets the user.
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.message.content, user_id, server_id, server_name)
    await ctx.send(f"{alert}Hi, you can use !help for a list of commands.")


# !help
@bot.command()
async def help(ctx):
    """
    Displays all commands.
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.message.content, user_id, server_id, server_name)
    embed = discord.Embed(
        title="Help", description="List of available commands:", color=0x00ff00)
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.cooldown(5, 20, commands.BucketType.user)
async def latency(ctx):
    """
    Shows latency to the bot.
    eg. !latency
    """
    bot_ping = round(ctx.bot.latency * 1000)
    server_id, server_name = get_server_details(ctx)
    user_id = get_user_id(ctx)
    log.command_executed(ctx.command.name, user_id, server_id, server_name)
    await ctx.send(f"{alert}🤖 {bot_ping} ms.")


@latency.error
async def latency_error(ctx, error):
    server_id, server_name = get_server_details(ctx)
    user_id = get_user_id(ctx)

    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = error.retry_after
        log.cooldown(ctx.command.name, user_id, server_id, server_name)
        await ctx.send(f'{alert}This command is on cooldown. Please try again in {remaining_time:.2f} seconds.')


# !list_members
@bot.command()
async def list_members(ctx):
    """
    List all members in the server.
    eg. !list_members
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.message.content, user_id, server_id, server_name)
    guild = ctx.guild
    members = guild.members
    member_list = f'{alert}List of members:\n'
    for member in members:
        member_list += f"{member.name}:\t{member}\n"
    await ctx.send(member_list)


# create_team
@bot.command()
async def create_team(ctx, name, *new_members):
    """
    Creates a team with members from the server.
    eg. !create_team [team_name] (member1#0000) (member2#0000) ...
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.message.content, user_id, server_id, server_name)
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
        response += f"\t - {member}\n"
    await ctx.send(response)


    # ------------------------------------------------------------------------ #
    # --- ESP Commands ------------------------------------------------------- #
    # ------------------------------------------------------------------------ #


# !status
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def status(ctx):
    """
    Displays national loadshedding status.
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.message.content, user_id, server_id, server_name)
    message = await response.status()
    await ctx.send(message)


@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = error.retry_after
        server_id, server_name = get_server_details(ctx)
        user_id = get_user_id(ctx)
        log.cooldown(ctx.command.name, user_id, server_id, server_name)
        await ctx.send(f'This command is on cooldown. Please try again in {remaining_time:.2f} seconds.')


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def area_search(ctx, name: str):
    """
    Searches for an area on Eskom se Push
    eg. !area_search stellenbosch
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.command.name, user_id, server_id, server_name)
    message = await response.search(name)
    await ctx.send(message)


@area_search.error
async def area_search_error(ctx, error):
    server_id, server_name = get_server_details(ctx)
    user_id = get_user_id(ctx)

    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = error.retry_after
        log.cooldown(ctx.command.name, user_id, server_id, server_name)
        await ctx.send(f'{alert}This command is on cooldown. Please try again in {remaining_time:.2f} seconds.')
    elif isinstance(error, commands.MissingRequiredArgument):
        log.arguments(ctx.command.name, user_id, server_id, server_name)
        await ctx.send(f'{alert}Please enter area name after search:\n!area_search Capetown')


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def area_add(ctx, area_id: str):
    """
    Adds an area to your user.
    eg. !area_search stellenbosch
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.command.name, user_id, server_id, server_name)
    user = schemas.CreateUser(name=user_id, area=area_id)
    _, result = user_db.create_user(user)
    await ctx.send(f"{alert}{result}")


@area_add.error
async def area_add_error(ctx, error):
    server_id, server_name = get_server_details(ctx)
    user_id = get_user_id(ctx)

    if isinstance(error, commands.CommandOnCooldown):
        remaining_time = error.retry_after
        log.cooldown(ctx.command.name, user_id, server_id, server_name)
        await ctx.send(f'{alert}This command is on cooldown. Please try again in {remaining_time:.2f} seconds.')
    elif isinstance(error, commands.MissingRequiredArgument):
        log.arguments(ctx.command.name, user_id, server_id, server_name)
        await ctx.send(f'{alert}Please enter area name after add:\n!area_add westerncape-2-universityofstellenbosch')


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def loadshedding(ctx):
    """
    Adds an area to your user.
    eg. !area_search stellenbosch
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.command.name, user_id, server_id, server_name)
    code, message, user = user_db.get_user_by_name(user_id)
    if code != 200:
        await ctx.author.send(f"{alert}{message}")
    if user['area'] != None:
        result = await response.area(user['area'])
        await ctx.author.send(result)
    else:
        await ctx.author.send(f"{alert}You have not set your location yet. (!area_add)")


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def schedule(ctx):
    """
    Shows your area's loadshedding schedule
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.command.name, user_id, server_id, server_name)
    code, message, user = user_db.get_user_by_name(user_id)
    if code != 200:
        await ctx.author.send(f"{alert}{message}")
    if user['area'] != None:
        result = await response.schedule(user['area'])
        await ctx.author.send(result)
    else:
        await ctx.author.send(f"{alert}You have not set your location yet. (!area_add)")



@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def quota(ctx):
    """
    Shows ESP quota
    eg. !quota
    """
    user_id = get_user_id(ctx)
    server_id, server_name = get_server_details(ctx)
    log.command_executed(ctx.command.name, user_id, server_id, server_name)
    result = await response.quota()
    await ctx.send(result)


# ---------------------------------------------------------------------------- #
# --- Run Bot ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def run_bot():
    bot.run(TOKEN)
