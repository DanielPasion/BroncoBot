import os
import discord
from dotenv import load_dotenv
from db import *
from PhotoSearchScraper import *
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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
        $$gamble: Randomly generate an instrcutor at CPP. To claim, react to the NAME OF THE PERSON (not the image) (1 roll per hour, rolls reset every hour,no claim cooldown)
        $$collection @user: Displays the collection of a user
        $$lookup 'instructor': Looks up if a specific person is in the database"""
        await message.channel.send(help_message)
    
    #Used to look up instructors to see if they're in the db
    if message.content.startswith('$$lookup'):
        request = message.content
        instructor = ""
        for i in range(9, len(request)):
            instructor += request[i]
        result = lookup_instructor_by_name(instructor)

        if result == False:
            await message.channel.send(instructor + " is not found in the database")
        else:
            await message.channel.send(instructor + " works for the " + result[0][2] + " department")
            await message.channel.send(file=discord.File(conver_b64(result[0][3]), 'image.png'))
            if ifclaimed(result[0][1]) != False:
                await message.channel.send("Instructor is claimed by: " + ifclaimed(instructor)[0])

    #Used to roll
    if message.content.startswith('$$gamble'):
        request = message.content
        random_number = random.randint(1, 1562)

        author = message.author
        server = message.guild.id
        if eligible_to_roll(str(author), server):
            instructordata = lookup_instructor_by_id(random_number)
            await message.channel.send(instructordata[1].replace("\n", ""))
            
            await message.channel.send("Member of the " + str(instructordata[2]) + " department")

            await message.channel.send(file=discord.File(conver_b64(instructordata[3]), 'image.png'))

            if ifclaimed(instructordata[1]) != False:
                await message.channel.send("Instructor is claimed by: " + ifclaimed(instructordata[1])[0])
        else:
            await message.channel.send("You have reached ur maximum rolls for the hour with 1 roll. Rolls reset at the :45 minute mark every hour!")

    #Used to roll
    if message.content.startswith('$$collection'):
        request = message.content
        user_id = ""
        for i in range(15, len(request)-1):
            user_id += request[i]

        server = message.guild
        mentioneduser = None
        for member in server.members:
            if str(member.id) == str(user_id):
                mentioneduser = member
                await message.channel.send(f"**{member.mention}'s collection: **")
        all_instructors = collection(str(mentioneduser))

        string_all_instructors = ""
        for i in all_instructors:
            string_all_instructors +="- " + i + "\n\n"
        await message.channel.send(string_all_instructors)

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

    #Too Slow
    if reaction.count > 1:
        await reaction.message.channel.send(f"You're too slow {mention}, someone beat you to it")

    elif ifclaimed(reaction.message.content) != False:
        await reaction.message.channel.send(f"Instructor is already owned")
    else:
        print("Here")
        mention = user.mention
        claim(str(user),str(reaction.message.guild.id),str(reaction.message.content))
        await reaction.message.channel.send(f"{mention}, you are now the proud owner of **{reaction.message.content}!!!**")
    






#Running the app
load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)