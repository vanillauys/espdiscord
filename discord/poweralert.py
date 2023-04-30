# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import discord
import asyncio
import os
import responses
from dotenv import load_dotenv
from typing import Tuple


# ---------------------------------------------------------------------------- #
# --- Discord Configuration -------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()
rsp = responses.Responses()


# ---------------------------------------------------------------------------- #
# --- Discord Events --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Bot():
    
    
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    CLIENT_ID = os.getenv('CLIENT_ID')
    TOKEN = os.getenv('TOKEN')


    async def send_message(self, message, command, user_message = None):
        try:
            response = rsp.handle_response(command, user_message)
            print(response)
            await message.channel.send(response)

        except Exception as e:
            await message.channel.send(rsp.error("An error occured. Please try again later."))
            print("an error occured")
            print(e)


    def run_discord_bot(self):
        client = discord.Client(intents=discord.Intents(value=68608).all())

        @client.event
        async def on_ready():
            print(f"{client.user} connected to Discord!")

        @client.event
        async def on_message(message):
            # Make sure bot doesn't get stuck in an infinite loop
            if message.author == client.user:
                return

            # Get data about the user
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")
            if user_message[0] != '!':
                return

            # Debug printing

            user_message = user_message[1:]  # [1:] Removes the '!'
            user_message = user_message.rstrip()
            if ' ' in user_message:
                command, user_message = user_message.split(" ", 1)
            else:
                command = user_message
                user_message = ''

            print(f"Command: {command}\nMessage: {user_message}")
            await self.send_message(message, command, user_message)

        client.run(self.TOKEN)