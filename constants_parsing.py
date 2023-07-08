import json

from utils.text_formatting import fmt_num


def getLevel(array, max_level, exp, overflow=0, start_location=0):
    compound = 0
    for level, xp_required in enumerate(array[start_location:], start=1):
        compound += xp_required
        if exp < float(compound):
            return level - 1
        if level > max_level:
            return max_level

    lvl = max_level
    if overflow != 0:
        while exp > compound:
            lvl += 1
            compound += overflow

    return lvl


def getGoldenDragLevel(exp):
    formatted = fmt_num(exp)

    compound = 0
    for level, xp_required in enumerate(constants['pet_level_xp'][20:], start=1):
        compound += xp_required
        if exp < float(compound):
            return level - 1, formatted

    lvl = 101
    compound += 5555
    while exp > compound and lvl != 200:
        lvl += 1
        compound += 1886700

    return lvl, formatted


def getSkillLevel(skill, value):
    formatted = fmt_num(value)

    levelling_data = 'skill_xp'
    if skill == 'runecrafting':
        levelling_data = 'runecrafting_xp'
    if skill == 'social2':
        levelling_data = 'social_xp'

    level = getLevel(constants[levelling_data], constants['leveling_caps'][skill], value)
    return level, formatted


def getCatacombsLevel(value):
    formatted = fmt_num(value)
    level = getLevel(constants['catacombs_xp'], 50, value, 200000000)

    return level, formatted


def getPetLevel(rarity, value):
    formatted = fmt_num(value)

    offset = constants["pet_rarity_offset"].get(rarity, 0)
    level = getLevel(constants['pet_level_xp'], 100, value, start_location=offset)

    if level == 0:
        level = 1
    return level, formatted


def getSlayerLevel(slayer, value):
    formatted = fmt_num(value)
    levelling_data = 'slayer'
    if slayer == 'vampire':
        levelling_data = 'vampire'

    level = getLevel(constants[levelling_data + '_xp'], constants['leveling_caps'][levelling_data], value)
    return level, formatted


def getHotmLevel(value):
    formatted = fmt_num(value)
    level = getLevel(constants['hotm_xp'], 7, value)

    return level, formatted


with open('number_constants.json') as file:
    constants = json.load(file)
