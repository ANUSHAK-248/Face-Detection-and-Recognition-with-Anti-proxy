import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {    
    "databaseURL" : os.getenv("databaseURL"),   
    # "storageBucket" : "",
    })

ref = db.reference("Students")

tc = 25

# The schmea of the databse can be changes as per the requirements of organization
newdata = {
    "ELON_MUSK":{
        "name" : "Elon Musk",
        "sid" : "ELON_MUSK",
        "Specialisation" : "BUSINESS STRATEGIST, ENGINEER, GENIUS",        
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },    
}

# after running the code kindly move the data from new data to data object
data = {
    "SHAURYA_PATHANIA":{
        "name" : "Shaurya Pathania",             
        "sid" : "SHAURYA_PATHANIA",
        "Specialisation" : "B Tech - Mechanical",
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },    
    
    "ANUSHAK":{
        "name" : "Anushak Bhardwaj",             
        "sid" : "ANUSHAK",
        "Specialisation" : "All_Rounder",
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },
    
    "PRINCY_GARG":{
        "name" : "Princy Garg",             
        "sid" : "PRINCY_GARG",
        "Specialisation" :"CSE DS",
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },
    
    "KIRAN_JOT":{
        "name" : "Kiran Jot",             
        "sid" : "KIRAN_JOT",
        "Specialisation" : "CSE DS",
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },    
    
    "VARYAM_KAUR":{
        "name" : "Varyam Kaur",             
        "sid" : "VARYAM_KAUR",
        "Specialisation" : "CSE DS",
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },   
    
    "DOCTOR_STARNGE":{
        "name" : "Doctor Strange",
        "sid" : "DOCTOR_STARNGE",
        "Specialisation" : "NEURO NURGEON",        
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },
    
        
    "JACK_SPARROW":{
        "name" : "Jack Sparrow",
        "sid" : "JACK_SPARROW",
        "Specialisation" : "PIRATE, PRAGMATIST",        
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },
    
    "TONY_STARK":{
        "name" : "Tony Stark",
        "sid" : "TONY_STARK",
        "Specialisation" : "Engineering Skillset, Genius Billionaire",        
        "total attendance" : 0,
        "Working days" : tc,
        "last_attended" : "2024-03-18 14:10:15"
    },    
    
}

for key, value in newdata.items():
    ref.child(key).set(value)    

print("data of new person(s) has been uploaded")