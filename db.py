# Importing module 
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import random
from PhotoSearchScraper import *

#Getting password from .env file
load_dotenv()
PASSWORD = os.getenv("PASSWORD")

# Creating connection object
mydb = mysql.connector.connect(
    host = "broncobot.clklywpfer6l.us-east-2.rds.amazonaws.com",
    user = "admin",
    password = PASSWORD
)
 
# Printing the connection object and allowing queries
print("Connected to: ",mydb)


#Function to load all professors into the instructor table
def insert_instructor():
    #Use the teachers CSV file
    df = pd.read_csv('AllTeachers.csv')

    #Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")
    i = 1


    for term in df.values:
        query = "INSERT INTO Instructors (instructorID, name, department) VALUES (%s, %s, %s)"
        values = (i, term[0], term[1])
        cursor.execute(query, values)
        i += 1

    mydb.commit()
    cursor.close()

#Looks up instructor for the $$instructor command
def lookup_instructor_by_name(instructor):

    #Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")
    
    #Creating Query
    query = "SELECT * FROM Instructors WHERE name = '" + instructor + "'" 

    #Executing
    cursor.execute(query)

    result = cursor.fetchall()

    if len(result) == 0:
        return instructor + " is not in database"   
    else:
        return result

#Looks up instructor for the $$instructor command
def lookup_instructor_by_id(id):

    #Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")
    
    #Creating Query
    query = "SELECT * FROM Instructors WHERE instructorID = " + str(id) 
    #Executing
    cursor.execute(query)

    result = cursor.fetchall()

    return result[0]

#Looks up instructor for the $$instructor command
def eligible_to_roll(discordusername, discordserver):
    # Connecting to DB
    alternate = mysql.connector.connect(
        host = "broncobot.clklywpfer6l.us-east-2.rds.amazonaws.com",
        user = "admin",
        password = PASSWORD
    )
    mydb2 = mysql.connector.connect(
        host = "broncobot.clklywpfer6l.us-east-2.rds.amazonaws.com",
        user = "admin",
        password = PASSWORD
    )
    cursor = mydb2.cursor()
    cursor.execute("USE BroncoBot")
    # Creating Query
    query = "SELECT * FROM Rolls WHERE discordusername = '" + discordusername + "' and discordserver = " + str(discordserver)
    # Executing
    cursor.execute(query)
    result = cursor.fetchone()

    print(result)

    if result is None:
        insert = "INSERT INTO Rolls (discordusername, discordserver, rolls) VALUES (%s, %s, %s)"
        values = (discordusername, discordserver, 0)
        cursor.execute(insert, values)
        mydb2.commit()
        mydb2.close()
        return True
    elif result[2] == 2:
        return False
    else:
        rolls = result[2] + 1
        update = "UPDATE Rolls SET rolls = %s WHERE discordusername = %s and discordserver = %s"
        update_values = (rolls, discordusername, discordserver)
        cursor.execute(update, update_values)
        mydb2.commit()
        mydb2.close()
        return True
    
#Used to claim
def claim(discordusername, discordserver, instructor):
    # Restarting the server
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")

    #Get the instructor ID
    getID = "SELECT instructorID FROM Instructors WHERE name = '" + instructor + "'"
    cursor.execute(getID)
    instructorID = cursor.fetchone()[0]

    # Creating Insert Query but checking to see if they've been claimed first
    query = "INSERT INTO Claims (discordusername, discordserver, instructorID) VALUES (%s, %s, %s)"
    values = (discordusername, discordserver, instructorID)
    cursor.execute(query, values)
    mydb.commit()

    return True

#Used to claim
def collection(discordusername,discordserver):
    # Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")

    #Get the instructor ID
    query = "SELECT instructorID FROM Claims WHERE discordserver = '" + discordserver + "' AND discordusername= '" + discordusername + "'"
    cursor.execute(query)
    result = cursor.fetchall()

    print(result)
    #Get the names of all the instructors
    allinstructors = []
    for id in result:
        query = "SELECT name FROM Instructors WHERE instructorID = %s"
        cursor.execute(query,id)
        result = cursor.fetchone()[0]
        allinstructors.append(result)

    return allinstructors

#Function to load all professors into the instructor table
def insert_instructor_images():
    #Use the teachers CSV file
    df = pd.read_csv('AllTeachers.csv')

    #Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")
    i = 1


    for term in df.values:
        query = "INSERT INTO Instructors VALUES (%s, %s, %s, %s)"
        url = lookup_instructor(term[0])
        print(url)
        values = (i, term[0], term[1],url)
        cursor.execute(query, values)
        i += 1

    mydb.commit()
    cursor.close()

#Function to load all professors into the instructor table
def ifclaimed(instructor):

    #Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")

    #Finding if professorID
    query1 = "SELECT instructorID FROM Instructors WHERE name = '" + instructor + "'"
    cursor.execute(query1)
    result = cursor.fetchall()
    print(instructor)
    print(result)

    query2 = "SELECT discordusername FROM Claims WHERE instructorID = %s"
    try:
        cursor.execute(query2,result[0])
        result = cursor.fetchall()[0]
        mydb.commit()
        cursor.close()
        return result
    except:
        cursor.close()
        return False
