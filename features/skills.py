import json

import constants_parsing
from utils.text_formatting import printSmallHeader


with open('constants.json') as file:
    constants = json.load(file)


def getSkillData(player_data):
    total_level = 0
    for skill in constants['skills']:
        level, exp = constants_parsing.getSkillLevel(skill, player_data.get('experience_skill_' + skill, 0))

        # renaming weirdly named API skill
        if skill == 'social2':
            skill = 'social'

        # not counting either of these in the skill average
        if skill != 'social' and skill != 'runecrafting':
            total_level += level

        print(f'{skill.capitalize()} {level} with {exp} exp')

    printSmallHeader('Average Skill level')
    print('Average Skill Level:', round(total_level / 9, 2))
