from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from collections import Counter, OrderedDict
import pandas as pd


# Useful function to make sense of the raw data
def count_and_order(list_to_order) -> OrderedDict:
    return OrderedDict(Counter(list_to_order).most_common())

# Base class for all the different types of data
class DataObject():
    db_user = os.getenv("STDB_USER")
    db_password = os.getenv("STDB_PASS")
    client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@adonis.n0u0i.mongodb.net/Database?retryWrites=true&w=majority', server_api=ServerApi('1'))
    db = client.Database
    users = db.Users
    challenges = db.Challenges
    items = db.Items
    skills = db.Skills
    tasks = db.Tasks

    # Run after each call to close the connection with the Database
    def close(self) -> None:
        DataObject.client.close()

# Includes methods common to skills and challenges
class ActionData (DataObject):
    def __init__(self):
        self.data_type = None
        self.completed = None
        self.find_description = None

    #### NOT QUITE THERE YET. STILL HAVE TO FIGURE OUT HOW TO GO FROM ZIP TO DICT
    def id_to_goals(self, dictionary) -> dict:
        descriptions = [self.data_type.find_one({"_id":item})["goals"]for item in dictionary]
        # return list(zip(descriptions, list(dictionary.values())))

    def order_by_popularity(self, user_parameter={}) -> dict:
        # First create a list with the lists of skills that each user has completed and then unpack that list.
        list = [user[self.completed] for user in DataObject.users.find(user_parameter)]
        total_list = [item for sublist in list for item in sublist]
        return count_and_order(total_list)

class UserData (DataObject):
    # Count total users
    def count_users(self, parameter={}) -> int:
        return len(list(DataObject.users.find(parameter)))

    # Count users per timezone
    def timezone_counter(self, parameter={}) -> OrderedDict:
        # First create a list with the timezones each user has, then apply a Counter to it, and then package it all into an Ordered Dict
        return count_and_order([str(user["timezone"]) for user in DataObject.users.find(parameter)])
    
    # Dictonary with number of skills users have completed
    def number_skills_completed_dict(self, parameter={}) -> OrderedDict:
        return count_and_order([len(user["skillscompleted"]) for user in self.users.find(parameter)])
    
    # Describe the skills completed data
    def number_skills_completed_data(self, parameter={}) -> str:
        return pd.Series([len(user["skillscompleted"]) for user in self.users.find(parameter)]).describe()
    
    # Describe the days tracked data
    def days_tracked_data(self, parameter={}) -> str:
        return pd.Series([user["numDaysTracked"] for user in self.users.find(parameter)]).describe()

# SkillData object, inheriting from DataObject


### REWRITING ALL METHODS SUCH THAT THE RETURN IS IN TERMS OF ID. THAT WAY VARIOUS WAYS OF RETURNING DATA WITH EXTRA METHODS
class SkillData(ActionData):
    def __init__(self):
        super().__init__()
        self.data_type = DataObject.skills
        self.completed = "skillscompleted"

    def id_to_title_and_level(self, dictionary) -> dict:
        title_and_id = [(self.data_type.find_one({"_id":item})["title"], self.data_type.find_one({"_id":item})["level"])  for item in dictionary]
        return dict(zip(title_and_id, dictionary.values()))

    ## REWRITING THIS METHOD
    def order_skills_by_popularity(self, user_parameter={}) -> list:

        # First create a list with the lists of skills that each user has completed and then unpack that list.
        skill_list = [user["skillscompleted"] for user in self.users.find(user_parameter)]

        ### FIX TOTAL_LIST (FOR THE MOMENT IT RETURNS SKILL_LIST). USE INDECES
        total_list = [skill for skill in skill_list]
        total_dictionary = count_and_order(total_list)
        skills = total_dictionary.keys()
        
        skill_descriptions = [self.skills.find_one({"_id":skill})["goals"] for skill in skills]
        title_count = dict(zip(skill_descriptions, total_dictionary.values()))
        
        return title_count
    
    def get_skill_completion_rate(self, user_parameter={}, skill_parameter={}) -> dict:
        from collections import Counter
        users = self.users.find(user_parameter)
        skills = [skill["_id"] for skill in self.skills.find(skill_parameter)]
        completed_list = []
        progress_list = []

        for user in users:
            for completed in user["skillscompleted"]:
               if completed in skills:
                    completed_list.append(completed)
            for progress in user["skillsinprogress"]:
                if progress in skills:
                    progress_list.append(progress)
        
        completed_counted = Counter(completed_list)
        progress_counted = Counter(progress_list)
        data_unordered = {key: {'Started': value + completed_counted[key], 'Progress': value, 'Completed': completed_counted[key], 'Score':float(completed_counted[key])/float(value+completed_counted[key])}  for (key, value) in progress_counted.items()}
        data_ordered = dict(sorted(data_unordered.items(), key=lambda x:x[1]['Score']))

        return data_ordered
    
    def list_skills_by_ease(self, skill_parameter={}) -> dict:
        data = self.get_skill_completion_rate(skill_parameter=skill_parameter)
        keys = [self.skills.find_one({"_id":id})["goals"][0] for id in data.keys()]
        values = [value['Score'] for value in data.values()]
        total_dict = dict(zip(keys, values))
        return total_dict
    

class ChallengeData(ActionData):
    def order_challenges_by_popularity(self, user_parameter={}) -> list:
        total_list = []
        users = self.users.find(user_parameter)
        for user in users:
            for challenge in user["challengescompleted"]:
                total_list.append(challenge)

        total_dictionary = OrderedDict(Counter(total_list).most_common())
        challenges = total_dictionary.keys()
        
        challenge_descriptions = [self.challenges.find_one({"_id":challenge})["goals"][0] for challenge in challenges]
        title_count = dict(zip(challenge_descriptions, total_dictionary.values()))
        
        return title_count
        
    def get_challenge_completion_rate(self, user_parameter={}, challenge_parameter={}) -> dict:
        users = self.users.find(user_parameter)
        challenges = [challenge["_id"] for challenge in self.challenges.find(challenge_parameter)]
        completed_list = []
        progress_list = []

        for user in users:
            for completed in user["challengescompleted"]:
               if completed in challenges:
                    completed_list.append(completed)
            for progress in user["challengesinprogress"]:
                if progress in challenges:
                    progress_list.append(progress)
        
        completed_counted = Counter(completed_list)
        progress_counted = Counter(progress_list)
        data_unordered = {key: {'Started': value + completed_counted[key], 'Progress': value, 'Completed': completed_counted[key], 'Score':float(completed_counted[key])/float(value+completed_counted[key])}  for (key, value) in progress_counted.items()}
        data_ordered = dict(sorted(data_unordered.items(), key=lambda x:x[1]['Score']))

        return data_ordered

    def get_challenge_ease(self, challenge_parameter={}) -> dict:
        data = self.get_challenge_completion_rate(challenge_parameter=challenge_parameter)
        keys = [self.challenges.find_one({"_id":id})["goals"][0] for id in data.keys()]
        values = [value['Score'] for value in data.values()]
        total_dict = dict(zip(keys, values))
        return total_dict


print(SkillData().id_to_goals(SkillData().order_by_popularity()))
