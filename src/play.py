import stdata

r = stdata.Reader()

print(len(r.get_skill_completion_rate().keys()))
print(r.list_skills_by_ease(skill_parameter={'category':'MENTAL HEALTH'}))
r.graph_skills_by_popularity()