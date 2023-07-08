import json


def getLevel(array, max_level, exp, overflow=0):
    compound = 0
    for level, xp_required in enumerate(array, start=1):
        compound += xp_required
        if exp < float(compound):
            return level - 1
        if level > max_level:
            return max_level

    lvl = len(array)
    if overflow != 0:
        while exp > compound:
            lvl += 1
            compound += overflow

    return lvl


def getSkillLevel(skill, value):
    formatted = format(int(value), ',')

    levelling_data = 'skill_xp'
    if skill == 'runecrafting':
        levelling_data = 'runecrafting_xp'
    if skill == 'social2':
        levelling_data = 'social_xp'

    level = getLevel(data[levelling_data], data['leveling_caps'][skill], value)
    return level, formatted


def getCatacombsLevel(value):
    formatted = format(int(value), ',')
    level = getLevel(data['catacombs_xp'], 50, value, 200000000)

    return level, formatted


def getSlayerLevel(slayer, value):
    formatted = format(int(value), ',')
    levelling_data = 'slayer'
    if slayer == 'vampire':
        levelling_data = 'vampire'

    level = getLevel(data[levelling_data + '_xp'], data['leveling_caps'][levelling_data], value)
    return level, formatted


def getHotmLevel(value):
    formatted = format(int(value), ',')
    level = getLevel(data['hotm_xp'], 7, value)

    return level, formatted


with open('number_constants.json') as file:
    data = json.load(file)
