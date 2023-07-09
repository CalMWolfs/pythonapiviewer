import json

from utils.text_utils import printSmallHeader, printHeader
from utils.api_utils import getPlayerData

from features import skills, dungeons, collections, accessories, pets, money, slayers, mining, general

username = input('Username: ')
data, uuid = getPlayerData(username)
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

printHeader('General Stats')
general.getSkyblockLevel(profile_specific)

printHeader('Skills')
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

# todo make not possibly null
printHeader('Coins')
# print money stuff
money.getPurse(profile_specific)
money.getBank(profile)

# get networth for user, not used rn but this is how you get the json that breaks down the networth categorically
# networth = requests.post(f'https://soopy.dev/api/v2/player_networth/{uuid}', json=data)
# networth_data = networth.json()

printHeader('Accessories')
# print magical power, selected power and tuning points allocation
accessories.getAccessoryData(accessories_data)

printHeader('Pets')
# only prints the pet stats for the 'important' pets, when not text based important pets should be removed
pets.getImportantPets(pet_data)
# prints general stats about pets, for now only pet score but more later
pets.getGeneralPetData(profile_specific)

printHeader('Slayers')
# print the data for slayers
slayers.getSlayerData(slayer_data)

printHeader('Mining')
# print hotm level
mining.getHotmLevel(mining_data)
# print powder stats for each
mining.getPowderStats(mining_data, 'mithril')
mining.getPowderStats(mining_data, 'gemstone')
# print info about the hotm perks
mining.getHotmPerks(mining_data)

