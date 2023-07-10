import json

import constants_parsing
from utils.text_utils import printSmallHeader, fmt_num, fmt_time

with open('constants.json') as file:
    constants = json.load(file)

total_runs = master_runs = 0


def getDungeonsLevel(dungeons_data):
    level, exp = constants_parsing.getCatacombsLevel(
        dungeons_data.get('dungeon_types', {}).get('catacombs', {}).get('experience', 0))
    print(f'Catacombs {level} with {exp} exp')


def getClassLevels(dungeons_data):
    for dungeon_class in constants['dungeons_classes']:
        level, exp = constants_parsing.getCatacombsLevel(
            dungeons_data.get('player_classes', {}).get(dungeon_class, {}).get('experience', 0))
        print(f'{dungeon_class.capitalize()} {level} with {exp} exp')


def getDungeonData(data, floor, master_mode):
    if master_mode:
        floor_name = f'Master Floor {floor}'
        completions = data.get('tier_completions', 0).get(str(floor), 0)
        if completions == 0:
            print(floor_name, 'has not been completed yet')
            return
        printSmallHeader(floor_name)

    else:
        floor_name = 'Entrance' if floor == 0 else f'Floor {floor}'

        completions = data.get('tier_completions', 0).get(str(floor), 0)
        if completions == 0:
            print(floor_name, 'has not been completed yet')
            return

        attempted = data.get('times_played', 0).get(str(floor), 0)
        if attempted == 0:
            print(floor_name, 'has not been attempted yet')
            return

        watcher_kills = data.get('watcher_kills', 0).get(str(floor), 0)
        printSmallHeader(floor_name)
        print('Times Attempted:', fmt_num(attempted))
        print('Watcher Kills:', fmt_num(watcher_kills))

    highest_score = data.get('best_score', 0).get(str(floor), 0)
    fastest_run = data.get('fastest_time', 0).get(str(floor), 0)
    fastest_s_plus = data.get('fastest_time_s_plus', 0).get(str(floor), 0)

    # save values for later
    if completions > 0:
        global total_runs
        total_runs += completions
        if master_mode:
            global master_runs
            master_runs += completions

    print('Times Completed:', fmt_num(completions))
    print('Best Score:', fmt_num(highest_score))
    print('Fastest S+ Run:', fmt_time(fastest_s_plus))
    print('Fastest Run:', fmt_time(fastest_run))


def getFloorData(dungeons_data):
    # todo maybe only say unattempted to one floor
    path = dungeons_data.get('catacombs', {})
    for floor in range(8):
        getDungeonData(path, floor, False)

    path = dungeons_data.get('master_catacombs', {})
    for floor in range(8):
        if floor == 0:
            continue
        getDungeonData(path, floor, True)

    printSmallHeader('Overall Stats')
    print('Total Runs Completed:', fmt_num(total_runs))
    print('Total Master Runs Completed:', fmt_num(master_runs))
    print('Secret count coming later')
