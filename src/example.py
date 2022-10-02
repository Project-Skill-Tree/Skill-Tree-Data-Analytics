'''
There are two modules that can be used to access the SkillTree data. 
We will begin by looking at stdata, which includes a series of methods whose
objective is to perform calculations using the raw data from the data compiling it into
more comprehensible formats.
'''
import stdata

'''
There are now various ways of proceeding. The way the stdata module is structured is very
simple. There is a class for UserData, one for SkillData and one for ChallengeData. Each of
these is equiped with a wide range of methods, which we must call in order to perform 
our analysis on the data. The easiest way of doing so is by creating an instance in place as follows.
'''

number_users = stdata.UserData().count_users()

'''
If you're going to call various methods of the UserData class, it might be better to use the 
following code.
'''

userData = stdata.UserData()
number_users = userData.count_users()
timezone_info = userData.timezone_counter()

'''
In order to make queries more interesting it can be very useful to make use of the parameters
that are available in each of the methods.
'''

# Completion rate of the skills belonging to the fitness category, where users are in timezone 0
data = stdata.SkillData().get_skill_completion_rate(skill_parameter={"category":"fitness"}, user_parameter={"timezone":0})
