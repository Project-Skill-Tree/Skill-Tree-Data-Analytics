from pymongo import MongoClient
from pymongo.server_api import ServerApi
import matplotlib.pyplot as plt
import os


class Reader (object):
    def __init__(self) -> None:
        db_user = os.getenv("STDB_USER")
        db_password = os.getenv("STDB_PASS")
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
        
        skill_descriptions = [self.skills.find_one({"_id":skill})["title"] for skill in skills]
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

    def order_challenges_by_popularity(self, user_parameter={}) -> list:
        from collections import Counter, OrderedDict
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
    
    def graph_challenges_by_popularity(self, user_parameter={}, amount=10, graph_all=False, tight_layout=True) -> None:
        uncut_data = self.order_challenges_by_popularity(user_parameter)

        if graph_all == True:
            amount = len(uncut_data) + 1

        data = {k: uncut_data[k] for k in list(uncut_data)[:amount]}
        challenges = list(data.keys())
        performance = list(data.values())
        plt.style.use("seaborn-darkgrid")
        plt.barh(challenges, performance)
        plt.xlabel('Number of completions')
        plt.title('Challenge Popularity')

        for i, v in enumerate(performance):
            plt.text(v + 1, i, str(v), color='blue', fontweight='bold')
        
        if tight_layout:
            plt.tight_layout()

        plt.show()
    
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
                if completed in skills:
                    progress_list.append(progress)
        
        completed_counted = Counter(completed_list)
        progress_counted = Counter(progress_list)
        data_unordered = {key: {'Started': value + completed_counted[key], 'Progress': value, 'Completed': completed_counted[key], 'Score':float(completed_counted[key])/float(value+completed_counted[key])}  for (key, value) in progress_counted.items()}
        data_ordered = dict(sorted(data_unordered.items(), key=lambda x:x[1]['Score']))

        return data_ordered
    
    def list_skills_by_ease(self, skill_parameter={}):
        data = self.get_skill_completion_rate(skill_parameter=skill_parameter)
        keys = [self.skills.find_one({"_id":id})["title"] for id in data.keys()]
        values = [value['Score'] for value in data.values()]
        total_dict = dict(zip(keys, values))
        return total_dict

    def close(self) -> None:
        self.client.close()
