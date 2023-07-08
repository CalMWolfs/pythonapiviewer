import requests
import json

from secrets import API_KEY
import constants_parsing


def printHeader(text):
    print(f'\n-------------------------------------\n{text}\n-------------------------------------')


def printSmallHeader(text):
    print(f'------------{text}------------')


def fetchData():
    try:
        username = input('Username: ')
        print('Getting player UUID')
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        response.raise_for_status()
        player_uuid = response.json()['id']
        print(f'THe uuid for {username} is: {player_uuid}')
        print('Getting player data from the Hypixel API')
        response = requests.get('https://api.hypixel.net/skyblock/profiles?key=' + API_KEY + '&uuid=' + player_uuid)
        response.raise_for_status()
        return response.json().get('profiles', []), player_uuid

    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {str(e)}')
    except KeyError:
        print('Invalid username or user not found. Please try again.')
    except json.JSONDecodeError:
        print('Invalid JSON received.')


data, uuid = fetchData()
# Todo make function for getting from json so can handle errors there. Also cache data somehow between runs of
#  the program, maybe on start check creation date of each cached user and git ignore the folder
#  deal with disabled api

if data:
    for index, profile in enumerate(data, start=1):
        fruit = profile.get('cute_name', '')
        mode = profile.get('game_mode', 'Classic')
        level = profile.get('members', {}).get(uuid, {}).get('leveling', {}).get('experience', 0) / 100
        selected = '  Currently Selected' if profile.get('selected', '') else ''
        print(f'Profile {index}: {fruit} - {mode.capitalize()}, Level {level}{selected}')

    valid_input = False
    while not valid_input:
        user_input = input('Enter the profile number to access: ')
        index = int(user_input) - 1

        if 0 <= index < len(data):
            profile_data = data[index]
            fruit = profile_data.get('cute_name', '')
            mode = profile_data.get('game_mode', 'Classic')
            print(f'Selected: {fruit} - {mode}')
            valid_input = True
        else:
            print('Invalid input. Please try again.')

else:
    print('No profiles found for this user.')

profile_specific = profile_data['members'][uuid]
dungeons_data = profile_specific.get('dungeons', {})
accessories_data = profile_specific.get('accessory_bag_storage', {})
pet_data = profile_specific.get('pets', {})
slayer_data = profile_specific.get('slayer_bosses', {})
mining_data = profile_specific.get('mining_core', {})

with open('constants.json') as file:
    constants = json.load(file)

printHeader('SkyBlock level and Skill levels')
skyblock_level = profile_specific.get('leveling', {}).get('experience', 0) / 100
print(f'SkyBlock level: {skyblock_level}')

# todo deal with api off
for skill in constants['skills']:
    level, exp = constants_parsing.getSkillLevel(skill, profile_specific.get('experience_skill_' + skill, 0))
    if skill == 'social2':
        skill = 'social'
    print(f'{skill.capitalize()} {level} with {exp} exp')

printHeader('Dungeons')
level, exp = constants_parsing.getCatacombsLevel(
    dungeons_data.get('dungeon_types', {}).get('catacombs', {}).get('experience', 0))
print(f'Catacombs {level} with {exp} exp')

for dungeon_class in constants['dungeons_classes']:
    level, exp = constants_parsing.getCatacombsLevel(
        dungeons_data.get('player_classes', {}).get(dungeon_class, {}).get('experience', 0))
    print(f'{dungeon_class.capitalize()} {level} with {exp} exp')

printSmallHeader('Dungeons Runs')
total_completions = total_master_completions = 0

# todo better handling of things not being attempted/completed
for floor_num in range(8):
    runs = dungeons_data.get('dungeon_types', {}).get('catacombs', {}).get('tier_completions', {}).get(str(floor_num), 0)
    master_runs = dungeons_data.get('dungeon_types', {}).get('master_catacombs', {}).get('tier_completions', {}).get(str(floor_num), 0)
    total_completions += runs + master_runs
    total_master_completions += master_runs

    if runs + master_runs == 0:
        print(f'Floor {floor_num} not completed')
        continue
    if floor_num == 0:
        print(f'Entrance completed {format(int(runs), ",")} times')
        continue
    print(f'Floor {floor_num} completed {format(int(runs), ",")} times')
    if master_runs != 0:
        print(f'Master floor {floor_num} completed {format(int(master_runs), ",")} times')
    else:
        print(f'Master floor {floor_num} not completed')


print(f'Total dungeon completions: {format(int(total_completions), ",")}')
print(f'Total master mode completions: {format(int(total_master_completions), ",")}')
print('Secrets: Will do later')

# todo map api names to actual names
# todo collection lvl and maybe say if it is maxed?
printHeader('Collections')
for collection_type in constants['collections']:
    printSmallHeader(collection_type)
    output = ''
    for collection in constants['collections'][collection_type]:
        amount = format(profile_specific.get('collection', {}).get(collection, 0), ',')
        output += f'{collection}: {amount} '
    print(output)

# todo deal with bank api off (missing field in api)
printHeader('Coins')
print('Purse:', format(int(profile_specific.get('coin_purse', 0)), ','))
print('Bank:', format(int(profile.get('banking', {}).get('balance', 0)), ','))

printHeader('Accessories')
mp = accessories_data.get('highest_magical_power', 0)
print(f'Magical Power:', format(mp, ','))
print(f'Selected Power:', accessories_data.get('selected_power', 'None'))
printSmallHeader('Tuning Points')
for stat in accessories_data.get('tuning', {}).get('slot_0', {}):
    allocated = accessories_data.get('tuning', {}).get('slot_0', {}).get(stat, 0)
    if allocated != 0:
        print(f'{stat}:', allocated, 'points')

# todo only mark as important based on rarity (why does hypixel not use internal names here????)
printHeader('Pets')
for pet in pet_data:
    if pet.get('type', '') in constants['important_items']['pets']:
        # todo format stuff about the pet
        print(pet)

# todo map api name to display name e.g. zombie -> Revenant Horror
printHeader('Slayers')
for slayer in constants['slayers']:
    printSmallHeader(slayer)
    level, exp = constants_parsing.getSlayerLevel(slayer, slayer_data.get(slayer, {}).get('xp', 0))
    print(f'{slayer} {level} with {exp} exp')

    for tier in range(constants['highest_slayer_tier'][slayer]):
        kills = slayer_data.get(slayer, {}).get('boss_kills_tier_' + str(tier), 0)
        print(f'Tier {tier + 1} kills:', format(kills, ','))

# todo deal with api off?
#  deal with perks later and their mappings
#  maybe display total powder as well
#  maybe just say hotm maxed if 347,000 exp
#  calculate nucleus runs done through placed crystals?
printHeader('Heart of the Mountain')
level, exp = constants_parsing.getHotmLevel(mining_data.get('experience', 0))
print(f'HOTM {level} with {exp} exp')
print(f'Tokens Spent:', mining_data.get('tokens_spent', 0))
print('Mithril Powder Available:', format(mining_data.get('powder_mithril_total', 0), ','))
print('Mithril Powder Spent:', format(mining_data.get('powder_spent_mithril', 0), ','))
print('Gemstone Powder Available:', format(mining_data.get('powder_gemstone_total', 0), ','))
print('Gemstone Powder Spent:', format(mining_data.get('powder_spent_gemstone', 0), ','))
print('Pickaxe ability:', mining_data.get('selected_pickaxe_ability', 'None'))

# more later
