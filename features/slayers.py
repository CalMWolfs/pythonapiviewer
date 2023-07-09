import json

import constants_parsing
from utils.text_formatting import printSmallHeader, fmt_num


with open('constants.json') as file:
    constants = json.load(file)


def getSlayerData(data):
    for slayer in constants['slayers']:
        slayer_name = constants['slayers'].get(slayer, slayer)
        printSmallHeader(slayer_name)
        level, exp = constants_parsing.getSlayerLevel(slayer, data.get(slayer, {}).get('xp', 0))
        if exp == '0':
            print(f'No {slayer_name} progress')
            continue
        print(f'{slayer_name} {level} with {exp} exp')

        for tier in range(constants['highest_slayer_tier'][slayer]):
            kills = data.get(slayer, {}).get('boss_kills_tier_' + str(tier), 0)
            print(f'Tier {tier + 1} kills:', fmt_num(kills))
