'''
Provides useful methods regarding skills.
'''

import pandas as pd

def add_completed(skills, users) -> pd.DataFrame:
    '''
    Adds a column containing information on how many skills have been completed.
    '''
    skills["completed"] = 0
    for i, skill in skills.iterrows():
        id = skill["_id"]
        count = 0
        for j, user in users.iterrows():
            for completed in user["skillscompleted"]:
                if completed==id:
                    count += 1
        skills["completed"][i] = count

    return skills

def add_in_progress(skills, users):
    '''
    Adds a column containing information on how many skills have been completed.
    '''
    skills["completed"] = 0
    for i, skill in skills.iterrows():
        id = skill["_id"]
        count = 0
        for j, user in users.iterrows():
            for completed in user["skillsinprogress"]:
                if completed==id:
                    count += 1
        skills["completed"][i] = count

    return skills