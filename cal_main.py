import json

from utils.text_utils import printSmallHeader, printHeader
from utils.api_utils import getPlayerData, getSoopyNetworth
from utils.player_selection import selectProfile

from features import skills, dungeons, collections, accessories, pets, money, slayers, mining, general

username = input('Username: ')
player_data, uuid = getPlayerData(username)

profile_data, profile_num = selectProfile(player_data, uuid)

# todo run async
# networth_data = getSoopyNetworth(player_data, uuid)
# print(networth_data)

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

printHeader('Coins')
# print money stuff
money.getPurse(profile_specific)
money.getBank(player_data[profile_num])

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
