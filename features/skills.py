import json

import constants_parsing
from utils import text_formatting


def getSkillData(player_data):
    total_level = 0
    for skill in constants['skills']:
        level, exp = constants_parsing.getSkillLevel(skill, player_data.get('experience_skill_' + skill, 0))
        if skill == 'social2':
            skill = 'social'

        if skill != 'social' and skill != 'runecrafting':
            total_level += level

        print(f'{skill.capitalize()} {level} with {exp} exp')
    text_formatting.printSmallHeader('Average Skill level')
    print('Average Skill Level:', round(total_level / 9, 2))


with open('constants.json') as file:
    constants = json.load(file)
