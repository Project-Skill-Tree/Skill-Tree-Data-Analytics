'''
Includes useful methods to process and analyse user data.
'''

import pandas as pd


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