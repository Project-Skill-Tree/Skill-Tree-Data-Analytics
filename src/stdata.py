from pymongo import MongoClient
from pymongo.server_api import ServerApi
import matplotlib.pyplot as plt
import os


class Reader (object):
    def __init__(self) -> None:
        db_user = os.environ.get("STDB_USER")
        db_password = os.environ.get("STDB_PASS")
        self.client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@adonis.n0u0i.mongodb.net/Database?retryWrites=true&w=majority', server_api=ServerApi('1'))
        self.db = self.client.Database
        self.users = self.db.Users
        self.challenges = self.db.Challenges
        self.items = self.db.Items
        self.skills = self.db.Skills
        self.tasks = self.db.Tasks

    
    def count_users(self, parameter={}) -> int:
        return len(list(self.users.find(parameter)))
    

    def order_skills_by_popularity(self, user_parameter={}) -> list:
        from collections import Counter, OrderedDict
        total_list = []
        users = self.users.find(user_parameter)
        for user in users:
            for skill in user["skillscompleted"]:
                total_list.append(skill)

        total_dictionary = OrderedDict(Counter(total_list).most_common())
        skills = total_dictionary.keys()
        
        skill_descriptions = [self.skills.find_one({"_id":skill})["goals"][0] for skill in skills]
        title_count = dict(zip(skill_descriptions, total_dictionary.values()))
        
        return title_count
    

    def graph_skills_by_popularity(self, user_parameter={}, amount=10, graph_all=False, tight_layout=True) -> None:
        uncut_data = self.order_skills_by_popularity(user_parameter)

        if graph_all == True:
            amount = len(uncut_data) + 1

        data = {k: uncut_data[k] for k in list(uncut_data)[:amount]}
        skills = list(data.keys())
        performance = list(data.values())
        plt.style.use("seaborn-darkgrid")
        plt.barh(skills, performance)
        plt.xlabel('Number of completions')
        plt.title('Skill Popularity')

        for i, v in enumerate(performance):
            plt.text(v + 1, i, str(v), color='blue', fontweight='bold')
        
        if tight_layout:
            plt.tight_layout()

        plt.show()


    def close(self) -> None:
        self.client.close()
