import requests
import json

from secrets import API_KEY
import constants_parsing
from utils.text_formatting import printSmallHeader, printHeader

from features import skills, dungeons, collections


def fetchData():
    try:
        username = input('Username: ')
        print('Getting player UUID')
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        response.raise_for_status()
        player_uuid = response.json()['id']
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
# todo Cache data somehow between runs of the program, maybe on start check creation date of each cached user and git
#  ignore the folder. Also deal with disabled api
#  maybe save as a custom json with only necessary info

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

# todo move
printHeader('SkyBlock level and Skill levels')
skyblock_level = profile_specific.get('leveling', {}).get('experience', 0) / 100
print(f'SkyBlock level: {skyblock_level}')

# Prints each skills experience and level along with skill average
skills.getSkillData(profile_specific)

printHeader('Dungeons')
# print dungeons level
dungeons.getDungeonsLevel(dungeons_data)
# print class levels
dungeons.getClassLevels(dungeons_data)
# print stats for each floor than overall stats
printSmallHeader('Dungeons Stats')
dungeons.getFloorData(dungeons_data.get('dungeon_types', {}))

printHeader('Collections')
# saves highest tier data for later
collections.saveCollectionLevel(profile_specific.get('unlocked_coll_tiers', {}))
# print the single player's collection count for each item
collections.getCollectionAmount(profile_specific.get('collection', {}))

# todo move
printHeader('Coins')
print('Purse:', format(int(profile_specific.get('coin_purse', 0)), ','))
print('Bank:', format(int(profile.get('banking', {}).get('balance', 0)), ','))

# get networth for user
# networth = requests.post(f'https://soopy.dev/api/v2/player_networth/{uuid}', json=data)
# networth_data = networth.json()

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
    # todo sort important pets, pet candies, pet item (needs to be mapped)
    pet_exp = pet.get('exp', 0)
    pet_rarity = pet.get('tier', '')

    if pet.get('type', '') == 'GOLDEN_DRAGON':
        level, exp = constants_parsing.getGoldenDragLevel(pet_exp)
    else:
        level, exp = constants_parsing.getPetLevel(pet_rarity, pet_exp)
    print(pet_rarity, pet.get('type', ''), f'lvl {level} with {exp} exp')

printHeader('Slayers')
for slayer in constants['slayers']:
    slayer_name = constants['slayers'].get(slayer, slayer)
    printSmallHeader(slayer_name)
    level, exp = constants_parsing.getSlayerLevel(slayer, slayer_data.get(slayer, {}).get('xp', 0))
    if exp == '0':
        print(f'No {slayer_name} progress')
        continue
    print(f'{slayer_name} {level} with {exp} exp')

    for tier in range(constants['highest_slayer_tier'][slayer]):
        kills = slayer_data.get(slayer, {}).get('boss_kills_tier_' + str(tier), 0)
        print(f'Tier {tier + 1} kills:', format(kills, ','))

# todo calculate nucleus runs done through placed crystals?
printHeader('Heart Of The Mountain')
level, exp = constants_parsing.getHotmLevel(mining_data.get('experience', 0))
if level == 7:
    print('HOTM 7')
else:
    print(f'HOTM {level} with {exp} exp')
print(f'Tokens Spent:', mining_data.get('tokens_spent', 0))
printSmallHeader('Mithril Powder')
spent = mining_data.get('powder_spent_mithril', 0)
available = mining_data.get('powder_mithril_total', 0)
print('Total:', format(available + spent, ','))
print('Available:', format(available, ','))
print('Spent:', format(spent, ','))
printSmallHeader('Gemstone Powder')
spent = mining_data.get('powder_spent_gemstone', 0)
available = mining_data.get('powder_gemstone_total', 0)
print('Total:', format(available + spent, ','))
print('Available:', format(available, ','))
print('Spent:', format(spent, ','))

# todo filter some of these perks
printSmallHeader('HOTM Perks')
ability_name = mining_data.get('selected_pickaxe_ability', 'None')
print('Selected pickaxe ability:', constants['hotm_perks'].get(ability_name, ability_name))
for perk in mining_data.get('nodes', {}):
    if 'toggle' in perk:
        continue
    perk_name = constants['hotm_perks'].get(perk, perk)
    print(perk_name + ': Level', mining_data.get('nodes', {}).get(perk, 0))

# more later
