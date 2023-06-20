from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import pandas as pd

def fetch_data(dir: str) -> None:
    '''
    Stores the data contained in the database locally.
    '''

    db_user = os.getenv("STDB_USER")
    db_password = os.getenv("STDB_PASS")
    client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@adonis.n0u0i.mongodb.net/Database?retryWrites=true&w=majority', server_api=ServerApi('1'))
    
    db = client.Database
    db_users = db.Users
    db_challenges = db.Challenges
    db_items = db.Items
    db_skills = db.Skills
    db_tasks = db.Tasks

    users = pd.DataFrame(list(db_users.find({})))
    challenges = pd.DataFrame(list(db_challenges.find({})))
    items = pd.DataFrame(list(db_items.find({})))
    skills = pd.DataFrame(list(db_skills.find({})))
    tasks = pd.DataFrame(list(db_tasks.find({})))

    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

    users.to_csv(dir+"/users.csv")
    challenges.to_csv(dir+"/challenges.csv")
    items.to_csv(dir+"/items.csv")
    skills.to_csv(dir+"/skills.csv")
    tasks.to_csv(dir+"/tasks.csv")

    client.close()

def read_data(dir: str) -> tuple:
    '''
    Returns the data as a tuple of Dataframes
    of users, challenges, items, skills and tasks.
    '''

    users = pd.read_csv(dir+"/users.csv")
    challenges = pd.read_csv(dir+"/challenges.csv")
    items = pd.read_csv(dir+"/items.csv")
    skills = pd.read_csv(dir+"/skills.csv")
    tasks = pd.read_csv(dir+"/tasks.csv")

    return users, challenges, items, skills, tasks
