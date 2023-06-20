from stdata import *
import matplotlib.pyplot as plt

class GraphObject():
    @staticmethod
    def set_plot(title: str, tight_layout: bool) -> None:
        plt.style.use("seaborn-darkgrid")
        plt.title(title)
        if tight_layout:
            plt.tight_layout
        plt.show()

class UserGraph(GraphObject):
    def graph_xp_distribution(self, user_parameter={}, tight_layout=True) -> None:
        xp_list = [user["xp"] for user in UserData().users.find(user_parameter)]
        plt.hist(xp_list)
        plt.yscale("log")
        self.set_plot("XP Distribution", tight_layout)

    def pie_timezones(self, user_parameter={}, tight_layout=True) -> None:
        data = UserData().timezone_counter(parameter=user_parameter)
        x = data.keys()
        y= data.values()
        plt.pie(y, labels=x)
        self.set_plot("Users per timezone", tight_layout)
    
    def bar_timezones(self, user_parameter={}, tight_layout=True) -> None:
        data = UserData().timezone_counter(parameter=user_parameter)
        x = data.keys()
        y = data.values()
        plt.bar(x, y)
        self.set_plot("Users per timezone", tight_layout)
    
    def graph_number_skills_completed(self, user_parameter={}, tight_layout=True) -> None:
        data = UserData().number_skills_completed_dict(parameter=user_parameter)
        x = data.keys()
        y = data.values()
        plt.bar(x, y)
        self.set_plot("Number of skills completed", tight_layout)

class SkillGraph(GraphObject):
    def graph_skills_by_popularity(self, user_parameter={}, amount=10, graph_all=False, tight_layout=True) -> None:
        uncut_data = SkillData().order_skills_by_popularity(user_parameter)

        if graph_all == True:
            amount = len(uncut_data) + 1

        data = {k: uncut_data[k] for k in list(uncut_data)[:amount]}
        skills = list(data.keys())
        performance = list(data.values())
        plt.barh(skills, performance)
        plt.xlabel('Number of completions')

        for i, v in enumerate(performance):
            plt.text(v + 1, i, str(v), color='blue', fontweight='bold')
        
        self.set_plot("Skill Popularity", tight_layout)
    
    def graph_skills_by_ease(self, skill_parameter={}, tight_layout=False, amount=10) -> None:
        data = SkillData().list_skills_by_ease(skill_parameter=skill_parameter)
        plt.barh( list(data.keys())[:amount], list(data.values())[:amount])
        plt.xlabel("Completion_rate")
        self.set_plot("Skills by ease", tight_layout=tight_layout)

class ChallengeGraph(GraphObject):
    def graph_challenges_by_popularity(self, user_parameter={}, amount=10, graph_all=False, tight_layout=True) -> None:
        uncut_data = ChallengeData().order_challenges_by_popularity(user_parameter)

        if graph_all == True:
            amount = len(uncut_data) + 1

        data = {k: uncut_data[k] for k in list(uncut_data)[:amount]}
        challenges = list(data.keys())
        performance = list(data.values())
        plt.barh(challenges, performance)
        plt.xlabel('Number of completions')

        for i, v in enumerate(performance):
            plt.text(v + 1, i, str(v), color='blue', fontweight='bold')
        
        self.set_plot("Challenge Popularity", tight_layout)
