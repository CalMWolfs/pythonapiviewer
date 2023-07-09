import json

from utils.text_utils import printSmallHeader, fmt_num


with open('constants.json') as file:
    constants = json.load(file)


def getAccessoryData(data):
    magical_power = data.get('highest_magical_power', 0)
    print(f'Magical Power:', fmt_num(magical_power))
    # todo try to get the stats from this based on mp
    print(f'Selected Power:', data.get('selected_power', 'None'))

    printSmallHeader('Allocated Tuning Points')

    # only showing stats with at least 1 allocated point
    # todo maybe show the stat increase e.g. 4 points in int is 8 int
    for stat in data.get('tuning', {}).get('slot_0', {}):
        allocated = data.get('tuning', {}).get('slot_0', {}).get(stat, 0)
        if allocated != 0:
            print(constants['tuning_points'].get(stat, stat) + ':', allocated, 'points')
