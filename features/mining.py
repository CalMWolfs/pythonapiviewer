import json

import constants_parsing
from utils.text_formatting import printSmallHeader, fmt_num


with open('constants.json') as file:
    constants = json.load(file)


def getHotmLevel(data):
    level, exp = constants_parsing.getHotmLevel(data.get('experience', 0))
    if level == 7:
        print('Heart Of The Mountain Level 7')
    else:
        print(f'Heart Of The Mountain Level {level} with {exp} exp')


def getPowderStats(data, name):
    printSmallHeader(f'{name.capitalize()} Powder')
    spent = data.get('powder_spent_' + name, 0)
    available = data.get('powder_' + name + '_total', 0)
    print('Total:', format(available + spent, ','))
    print('Available:', format(available, ','))
    print('Spent:', format(spent, ','))


def getHotmPerks(data):
    printSmallHeader('HOTM Perks')
    print(f'Tokens Spent:', data.get('tokens_spent', 0))

    ability = data.get('selected_pickaxe_ability', 'None')
    print('Selected pickaxe ability:', constants['hotm_perks'].get(ability, ability))

    for perk in data.get('nodes', {}):
        if 'toggle' in perk:
            continue
        perk_name = constants['hotm_perks'].get(perk, perk)
        print(perk_name + ': Level', data.get('nodes', {}).get(perk, 0))

