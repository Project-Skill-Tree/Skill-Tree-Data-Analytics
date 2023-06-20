'''
Includes useful methods to process and analyse user data.
'''

import pandas as pd
import numpy as np


def process(users: pd.DataFrame) -> pd.DataFrame:
    '''
    Deletes unnecessary information and modifies certain columns.
    '''
    users = users.drop(["__v", "discordid", "Unnamed: 0"], axis=1)
    users["reminderSent"] = users["reminderSent"].replace({True: 1, False: -1})
    return users

def active(users: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a new Dataframe including only active users.
    '''
    return users[users["numDaysTracked"] > 0]

def non_null(users: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a new Dataframe including only users with non-null xp.
    '''
    return users[users["xp"] != 0]

def null(users: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a new Dataframe including only users with null xp.
    '''
    return users[users["xp"] == 0]

def current(users: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a new Dataframe including only users who have tracked in the week prior to 
    the current date.
    '''
    raise NotImplementedError

def coeff_variation(users: pd.DataFrame, field: str) -> pd.DataFrame:
    '''
    Calculates the coefficient of variation of users for a given field.
    '''
    return users[field].std()/users[field].mean()

def add_completions_per_category(users: pd.DataFrame, skills: pd.DataFrame) -> pd.DataFrame:
    '''
    Adds a new column per category of skills detailing the amount of completions each user has
    for that given category.
    '''
    import ast
    import re
    users_extended = users
    for category in skills["category"].unique():
        users_extended.loc[:, category+"C"] = 0
    
    for i, user in users_extended.iterrows():
        clean_str = re.sub(r"ObjectId\('(.+?)'\)", r"'\1'", user["skillscompleted"])
        for completed in ast.literal_eval(clean_str):
            skill = skills[skills["_id"] == completed]
            category = skill["category"]
            users_extended.at[i, category+"C"] = users_extended.loc[i, category+"C"] + 1
    return users_extended

def add_skills_completed(users:pd.DataFrame, skills:pd.DataFrame) -> pd.DataFrame:
    '''
    Adds a new column per skill indicating wether the user has completed said skill.
    '''
    import re
    import ast

    users_extended = users
    for i, skill in skills.iterrows():
        users_extended.loc[:, skill["title"]] = 0
    
    for i, user in users_extended.iterrows():
        clean_str = re.sub(r"ObjectId\('(.+?)'\)", r"'\1'", user["skillscompleted"])
        for completed in ast.literal_eval(clean_str):
            skill = skills[skills["_id"] == completed]
            users_extended.at[i, skill["title"]] = users_extended.loc[i, skill["title"]] + 1

    return users_extended

def distance(user1: pd.Series, user2: pd.Series, skills: pd.DataFrame) -> float:
    '''
    Calculates the completion distance between two users. 
    
    Note that the completion rates must have been added.
    '''
    user1_vect = user1[[title for title in skills["title"].unique()]]
    user2_vect = user2[[title for title in skills["title"].unique()]]
    return np.sqrt(np.array(user1_vect)@np.array(user2_vect))

def epsilon_neighborhood(user:pd.DataFrame, users:pd.DataFrame, skills:pd.DataFrame, epsilon:float) -> pd.DataFrame:
    '''
    Returns a DataFrame containing all the users that are at a certain distance away from a given user.

    Note that the completion rates must have been added.
    '''
    series = []
    for i, user2 in users.iterrows():
        if user2["_id"] != user["_id"]:
            if distance(user, user2, skills) <= epsilon:
                series.append(user2)

    return pd.DataFrame(series)

