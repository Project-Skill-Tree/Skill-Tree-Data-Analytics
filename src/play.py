import stdata
import stgraphs

oso = stdata.SkillData().order_by_popularity()
print(stdata.SkillData().id_to_title_and_level(oso))