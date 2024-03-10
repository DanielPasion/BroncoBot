import os
import discord
from dotenv import load_dotenv
from db import *
from datetime import datetime, timedelta

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

    #Help Command
    if message.content.startswith('$$help'):
        help_message = """Welcome to Bronco Bot! If you have any other questions, please contact .thedaniel on discord. Here are a list of commands you can do:

        $$help: Send a list of commands
        $$gamble: Randomly generate an instrcutor at CPP. To claim, react to the message that was sent (7 rolls per hour, rolls reset every hour on the dot,no claim cooldown)
        $$collection @user: Displays the collection of a user
        $$lookup 'instructor': Looks up if a specific person is in the database"""
        await message.channel.send(help_message)
    
    #Used to look up instructors to see if they're in the db
    if message.content.startswith('$$lookup'):
        request = message.content
        instructor = ""
        for i in range(9, len(request)):
            instructor += request[i]
        await message.channel.send(lookup_instructor_by_name(instructor))

    #Used to roll
    if message.content.startswith('$$gamble'):
        request = message.content
        random_number = random.randint(1, 1562)

        author = message.author
        server = message.guild.id
        if eligible_to_roll(str(author), server):
            await message.channel.send(lookup_instructor_by_id(random_number))
        else:
            await message.channel.send("You have reached ur maximum rolls for the hour with 7 rolls. Next roll reset is at: (figure out how to do roll resets later)")

@client.event
#Used to claim
async def on_reaction_add(reaction, user):
    if reaction.message.author != client.user:
        return
    
    #Calculating Reaction Time
    message_time = reaction.message.created_at - timedelta(hours=7)
    message_time = message_time.replace(tzinfo=None)
    reaction_time = datetime.now().replace(tzinfo=None)
    time_difference = reaction_time-message_time

    print(reaction.count)
    #Too Slow
    if reaction.count > 1:
        await reaction.message.channel.send(f"You're too slow {mention}, someone beat you to it")

    elif time_difference > timedelta(seconds=10):
        mention = user.mention
        await reaction.message.channel.send(f"You're too slow {mention}, you missed the 10 second window mark and reacted to the message in: " + str(time_difference))

    else:
        print()
    






#Running the app
load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)