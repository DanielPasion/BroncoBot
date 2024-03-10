# Importing module 
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

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
def lookup_instructor(instructor):

    #Connecting to DB
    cursor = mydb.cursor()
    cursor.execute("USE BroncoBot")
    
    #Creating Query
    query = "SELECT * FROM Instructors WHERE name = '" + instructor + "'" 

    #Executing
    cursor.execute(query)

    result = cursor.fetchall()

    print(result)
    if len(result) == 0:
        return instructor + " is not in database"   
    else:
        return instructor + " works for the " + result[0][2] + " department"
#insert_instructor()