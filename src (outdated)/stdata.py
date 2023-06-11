from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from collections import Counter, OrderedDict
import pandas as pd

################ CREATE GET SCV


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
        self.progress = None
        self.find_description = None

    def id_to_goals(self, dictionary) -> dict:
        descriptions = [self.data_type.find_one({"_id":item})["goals"]for item in dictionary]
        return list(zip(descriptions, list(dictionary.values())))

    def order_by_popularity(self, user_parameter={}) -> dict:
        # First create a list with the lists of skills that each user has completed and then unpack that list.
        list = [user[self.completed] for user in DataObject.users.find(user_parameter)]
        total_list = [item for sublist in list for item in sublist]
        return count_and_order(total_list)

    def get_completion_rate(self, user_parameter={}, action_parameter={}) -> dict:
        from collections import Counter
        users = self.users.find(user_parameter)
        items = [item["_id"] for item in self.data_type.find(action_parameter)]
        completed_list = []
        progress_list = []

        for user in users:
            for completed in user[self.completed]:
               if completed in items:
                    completed_list.append(completed)
            for progress in user[self.progress]:
                if progress in items:
                    progress_list.append(progress)
        
        completed_counted = Counter(completed_list)
        progress_counted = Counter(progress_list)
        data_unordered = {key: {'Started': value + completed_counted[key], 'Progress': value, 'Completed': completed_counted[key], 'Score':float(completed_counted[key])/float(value+completed_counted[key])}  for (key, value) in progress_counted.items()}
        data_ordered = dict(sorted(data_unordered.items(), key=lambda x:x[1]['Score']))

        return data_ordered
    
    def get_ease(self, action_parameter={}) -> dict:
        data = self.get_completion_rate(action_parameter=action_parameter)
        keys = [self.data_type.find_one({"_id":id})["goals"][0] for id in data.keys()]
        values = [value['Score'] for value in data.values()]
        total_dict = dict(zip(keys, values))
        return total_dict


class UserData (DataObject):
    def count_users(self, parameter={}) -> int:
        return len(list(DataObject.users.find(parameter)))

    def timezone_counter(self, parameter={}) -> OrderedDict:
        return count_and_order([str(user["timezone"]) for user in DataObject.users.find(parameter)])
    
    def number_skills_completed_dict(self, parameter={}) -> OrderedDict:
        return count_and_order([len(user["skillscompleted"]) for user in self.users.find(parameter)])
    
    def number_skills_completed_data(self, parameter={}) -> str:
        return pd.Series([len(user["skillscompleted"]) for user in self.users.find(parameter)]).describe()
    
    def days_tracked_data(self, parameter={}) -> str:
        return pd.Series([user["numDaysTracked"] for user in self.users.find(parameter)]).describe()


class SkillData(ActionData):
    def __init__(self):
        super().__init__()
        self.data_type = DataObject.skills
        self.completed = "skillscompleted"
        self.progress = "skillsinprogress"

    def id_to_title_and_level(self, dictionary) -> dict:
        title_and_id = [(self.data_type.find_one({"_id":item})["title"], self.data_type.find_one({"_id":item})["level"])  for item in dictionary]
        return dict(zip(title_and_id, dictionary.values()))

    def get_skills_csv(self) -> None:
        import csv
        data = self.get_completion_rate()
        titles = list(self.id_to_title_and_level(data).keys())
        goals = [item[0] for item in self.id_to_goals(data)]
        started = [data[datum]["Started"] for datum in data]
        progress = [data[datum]["Progress"] for datum in data]
        completed = [data[datum]["Completed"] for datum in data]
        score = [data[datum]["Score"] for datum in data]
        rows = [[titles[i], goals[i], started[i], progress[i], completed[i], score[i]] for i in range(len(titles))]
        
        with open('skills.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f, delimiter=';')
            for row in rows:
                writer.writerow(row)

class ChallengeData(ActionData):
    def __init__(self):
        super().__init__()
        self.data_type = DataObject.challenges
        self.completed = "challengescompleted"
        self.progress = "challengesinprogress"

SkillData().get_skills_csv()