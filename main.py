import os
import discord
from dotenv import load_dotenv
from db import *

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    #Used to ignore messages sent by the bot
    if message.author == client.user:
        return

    if message.content.startswith('$$help'):
        help_message = """Welcome to Bronco Bot! If you have any other questions, please contact .thedaniel on discord. Here are a list of commands you can do:

        $$help: Send a list of commands
        $$gamble: Randomly generate an instrcutor at CPP. To claim, react to the message that was sent (7 rolls per hour, rolls reset every hour on the dot,no claim cooldown)
        $$collection @user: Displays the collection of a user
        $$lookup 'instructor': Looks up if a specific person is in the database"""
        await message.channel.send(help_message)
    
    if message.content.startswith('$$lookup'):
        request = message.content
        instructor = ""
        for i in range(9, len(request)):
            instructor += request[i]
        await message.channel.send(lookup_instructor(instructor))









#Running the app
load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)