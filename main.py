import requests
import json
import base64
import gzip
import io
from pynbt import NBTFile
from secrets import API_KEY

while True:
    try:
        username = input('Username: ')
        print('Pinging Mojang API')
        url = f'https://api.mojang.com/users/profiles/minecraft/{username}?'
        response = requests.get(url)
        response.raise_for_status()  # Check for any HTTP errors
        trimid = response.json()['id']
        response_timemojang = response.elapsed.total_seconds()  # Calculate the response time in seconds
        print('Response time:', response_timemojang, 'seconds')
        apikey = API_KEY
        print('UUID is', trimid)
        print('Pinging Hypixel API...')
        headers = {'Accept': 'skyblock/profiles?key=' + apikey + '&uuid=' + trimid}
        resp = requests.get('https://api.hypixel.net/skyblock/profiles?key=' + apikey + '&uuid=' + trimid)
        response = requests.get('https://api.hypixel.net/player?uuid=' + trimid + '&key=' + apikey)
        secrets = response.json()
        resp.raise_for_status()  # Check for any HTTP errors
        data = resp.json()
        x = data.get('profiles', [])
        response_time = resp.elapsed.total_seconds()  # Calculate the response time in seconds
        print('Response time:', response_time, 'seconds')
        break  # Exit the loop if all API requests are successful
    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {str(e)}')
        # Handle the error gracefully
    except KeyError:
        print('Invalid username or user not found. Please try again.')
        # Prompt the user to re-enter their username if it is invalid, won't work on all errors though
    except json.JSONDecodeError:
        print('Invalid response from the Hypixel API. Please try again.')
        # Handle the case where the response from the Hypixel API is not valid JSON

if x:
    for index, profile in enumerate(x, start=1):
        profile_id = profile.get('profile_id', '')
        cute_name = profile.get('cute_name', '')
        gamemode = profile.get('game_mode', 'Classic')
        print(f'Profile {index}: Profile ID - {profile_id}, - {cute_name} - Type: {gamemode}')

    valid_input = False
    while not valid_input:
        user_input = input('Enter the profile number to access: ')
        index = int(user_input) - 1

        if 0 <= index < len(x):
            yes = x[index]
            profile_id = yes.get('profile_id', '')
            cute_name = yes.get('cute_name', '')
            gamemode = yes.get('game_mode', 'Classic')
            print(f'Selected Profile: Profile ID - {profile_id}, - {cute_name} - Type: {gamemode}')
            valid_input = True
        else:
            print('Invalid input or index out of range. Please try again.')
else:
    print('No profiles found for this user.')




print('------------------------\nDungeon Experience\n------------------------')
cataxp = yes['members'][trimid]['dungeons']['dungeon_types']['catacombs'].get('experience')
healxp = yes['members'][trimid]['dungeons']['player_classes'].get('healer', {}).get('experience')
magexp = yes['members'][trimid]['dungeons']['player_classes'].get('mage', {}).get('experience')
bersxp = yes['members'][trimid]['dungeons']['player_classes'].get('berserk', {}).get('experience')
archxp = yes['members'][trimid]['dungeons']['player_classes'].get('archer', {}).get('experience')
tankxp = yes['members'][trimid]['dungeons']['player_classes'].get('tank', {}).get('experience')

if all((cataxp, healxp, magexp, bersxp, archxp, tankxp)):
    print('Catacombs XP:', cataxp)
    print('Healer XP:', healxp)
    print('Mage XP:', magexp)
    print('Berserk XP:', bersxp)
    print('Archer XP:', archxp)
    print('Tank XP:', tankxp)
else:
    print('Lack of Catacombs experience or class experience!')
print('------------------------\nDungeon Runs & Secrets\n------------------------')
tier_completions = yes['members'][trimid]['dungeons']['dungeon_types'].get('catacombs', {}).get('tier_completions', {})

for floor_num in range(8):
    completions = tier_completions.get(str(floor_num), 0)
    if completions:
        print(f'Floor {floor_num}: {completions}')
    else:
        print(f'Floor {floor_num} not completed!')

    if floor_num == 0:
        f0 = completions
    elif floor_num == 1:
        f1 = completions
    elif floor_num == 2:
        f2 = completions
    elif floor_num == 3:
        f3 = completions
    elif floor_num == 4:
        f4 = completions
    elif floor_num == 5:
        f5 = completions
    elif floor_num == 6:
        f6 = completions
    elif floor_num == 7:
        f7 = completions

master_completions = yes['members'][trimid]['dungeons']['dungeon_types'].get('master_catacombs', {}).get('tier_completions', {})

for floor_num in range(1, 8):
    completions = master_completions.get(str(floor_num), 0)
    if completions:
        print(f'Master Floor {floor_num}: {completions}')
    else:
        print(f'Master Floor {floor_num} not completed!')

    if floor_num == 1:
        m1 = completions
    elif floor_num == 2:
        m2 = completions
    elif floor_num == 3:
        m3 = completions
    elif floor_num == 4:
        m4 = completions
    elif floor_num == 5:
        m5 = completions
    elif floor_num == 6:
        m6 = completions
    elif floor_num == 7:
        m7 = completions

total_master_runs = m1 + m2 + m3 + m4 + m5 + m6 + m7
print('Total Master Catacombs runs:', int(total_master_runs))
totalruns = f0 + f1 + f2 + f3 + f4 + f5 + f6 + f7
print('Total Catacombs runs:', int(totalruns))
runs = int(totalruns + total_master_runs)
print('Total Dungeon runs:', runs)
if 'player' in secrets:
    player_data = secrets['player']
    if 'achievements' in player_data:
        achievements = player_data['achievements']
        if 'skyblock_treasure_hunter' in achievements:
            treasure_hunter = achievements['skyblock_treasure_hunter']
            print('Secrets:', treasure_hunter)
        else:
            print('\'skyblock_treasure_hunter\' achievement not found.')
    else:
        print('No achievements found.')
else:
    print('No player data found.')
if runs == 0:
	print('Zero runs.')
else:
	print('Secrets/Run:', treasure_hunter/runs)
print('------------------------\nCollections\n------------------------')
collection = yes['members'][trimid].get('collection')
if collection:
    print(collection)
else:
    print('Disabled Collections or 0 collections unlocked!')
print('------------------------\nBank & Purse\n------------------------')
try:
	purse=yes['members'][trimid]['coin_purse']
	print('Purse:', purse)
except KeyError:
	print('0 coins?')
try:
	coopbank=yes['banking']['balance']
	print('Coop Bank:', coopbank)
except KeyError:
	print('Api disabled or 0 coins.')
print('------------------------\nAccessories\n------------------------')
try:
	power='Selected Power:', yes['members'][trimid]['accessory_bag_storage']['selected_power']
	mp='Magical Power:', yes['members'][trimid]['accessory_bag_storage']['highest_magical_power']
	print('Magical Power:', mp)
	print('Selected Power:', power)
	print('Tuning Points:', yes['members'][trimid]['accessory_bag_storage']['tuning']['slot_0'])
except KeyError:
	print('Disabled Api or 0 Talismans!')
print('------------------------\nSkyblock Level & Skill XP\n------------------------')
skills = ['combat', 'taming', 'farming', 'mining', 'foraging', 'fishing', 'enchanting', 'alchemy', 'carpentry', 'runecrafting', 'social2']

try:
    level = yes['members'][trimid]['leveling']['experience']
    for skill in skills:
        exp = yes['members'][trimid]['experience_skill_' + skill]
        print(f'{skill.capitalize()}: {exp}')
    print('Skyblock Level:', level/100)

    combat = yes['members'][trimid]['experience_skill_combat']
    if combat > 111672425:
        print(f'\nThis user is combat 60!')
    elif combat > 55172425:
        print(f'\nThis user is at least combat 50!')
    else:
        print(f'\nThis user\'s combat is not higher than level 50!')

    farming = yes['members'][trimid]['experience_skill_farming']
    if farming > 111672425:
        print(f'This user is farming 60!')
    elif farming > 55172425:
        print(f'This user is at least farming 50!')
    else:
        print(f'This user\'s farming is not higher than level 50!')

    mining = yes['members'][trimid]['experience_skill_mining']
    if mining > 111672425:
        print(f'This user is mining 60!')
    elif mining > 55172425:
        print(f'This user is at least mining 50!')
    else:
        print(f'This user\'s mining is not higher than level 50!')

    enchanting = yes['members'][trimid]['experience_skill_enchanting']
    if enchanting > 111672425:
        print(f'This user is enchanting 60!')
    elif enchanting > 55172425:
        print(f'This user is at least enchanting 50!')
    else:
        print(f'This user\'s enchanting is not higher than level 50!')

except KeyError:
    print('Api most likely disabled!')
print('------------------------\nPets\n------------------------')
try:
	petty=yes['members'][trimid]['pets']
except KeyError:
	print('Lack of Pets!')
print('Searching for important Pets:')
print('Golden Dragon')
print('Ender Dragon')
print('Spirit')
print('Silverfish')
print('Yeti')
print('Blue Whale\n')
search_terms = ['GOLDEN_DRAGON', 'ENDER_DRAGON', 'SPIRIT', 'SILVERFISH', 'BABY_YETI', 'BLUE_WHALE']
found_entries = [entry for entry in petty if entry['type'] in search_terms]

if found_entries:
    print("Important Pets found:")
    for entry in found_entries:
        print(entry)
else:
    print("None of the important pets required found.")
print('------------------------\nSlayers\n------------------------')
bosses = [ #easy to add new slayers
    ('Revenant Horror', 'zombie'),
    ('Tarantula Broodfather', 'spider'),
    ('Sven Packmaster', 'wolf'),
    ('Voidgloom Seraph', 'enderman'),
    ('Inferno Demonlord', 'blaze'),
    ('Riftstalker Bloodfiend', 'vampire')
]

for boss_name, boss_key in bosses:
    boss_data = yes['members'][trimid]['slayer_bosses'].get(boss_key, {})
    if boss_data:
        print(boss_name + ':')
        print('Levels:', boss_data.get('claimed_levels', 'No data found!'))
        print('Tier 1 Kills:', boss_data.get('boss_kills_tier_0', 'No data found!'))
        print('Tier 2 Kills:', boss_data.get('boss_kills_tier_1', 'No data found!'))
        print('Tier 3 Kills:', boss_data.get('boss_kills_tier_2', 'No data found!'))
        print('Tier 4 Kills:', boss_data.get('boss_kills_tier_3', 'No data found!'))
        if boss_key != 'spider' and boss_key != 'wolf' and boss_key != 'enderman' and boss_key != 'blaze': #no tier 5 variants yet
            print('Tier 5 Kills:', boss_data.get('boss_kills_tier_4', 'No data found!'))
        print('Total XP:', boss_data.get('xp', 'No XP Data!'))
    else:
        print(f'No data found for {boss_name}!')
print('------------------------\nHeart of the Mountain Stats\n------------------------')
mining_core_data = yes['members'][trimid].get('mining_core', {})
print('Heart of the Mountain Experience:', mining_core_data.get('experience', '0 Heart of the Mountain experience!'))
print('Tokens:', mining_core_data.get('tokens', '0 Tokens or value not present in User\'s API!'))
print('Tokens Spent:', mining_core_data.get('tokens_spent', '0 Tokens spent or value not present in User\'s API!'))
print('Mithril Powder:', mining_core_data.get('powder_mithril_total', '0 Mithril Powder!'))
print('Spent Mithril Powder:', mining_core_data.get('powder_spent_mithril', '0 Spent Mithril Powder'))
print('Gemstone Powder:', mining_core_data.get('powder_gemstone_total', '0 Gemstone Powder!'))
print('Spent Gemstone Powder:', mining_core_data.get('powder_spent_gemstone', '0 Spent Gemstone Powder!'))
print('Pickaxe ability:', mining_core_data.get('selected_pickaxe_ability', 'Lack of progression or ability!'))
print('------------------------\nHeart of the Mountain Perks\n------------------------')
desired_values = ['mining_speed', 'mining_fortune', 'mining_speed_2', 'mining_fortune_2', 'titanium_insanium', 'mining_speed_boost', 'daily_powder', 'efficient_miner', 'mining_experience', 'mining_madness', 'mole', 'professional', 'lonesome_miner', 'fortunate', 'great_explorer', 'powder_buff', 'vein_seeker', 'daily_effect', 'goblin_killer', 'forge_time', 'pickaxe_toss', 'fallen_star_bonus', 'experience_orbs', 'front_loaded', 'precision_mining', 'star_powder', 'maniac_miner', 'random_event', 'special_0']
found_values = {}
perk_names = {
	'mining_speed': 'Mining Speed 1',
	'mining_fortune': 'Mining Fortune 1',
	'mining_speed_2':  'Mining Speed 2',
	'mining_fortune_2':  'Mining Fortune 2',
	'titanium_insanium':  'Titanium Insanium',
	'mining_speed_boost':  'Mining Speed Boost',
	'daily_powder':  'Daily Powder',
	'efficient_miner':  'Efficient Miner',
	'mining_experience':  'Seasoned Mineman',
	'mining_madness':  'Mining Madness',
	'mole':  'Mole',
	'professional':  'Professional',
	'lonesome_miner':  'Lonesome Miner',
	'fortunate':  'Fortunate',
	'great_explorer':  'Great Explorer',
	'powder_buff':  'Powder Buff',
	'vein_seeker':  'Vein Seeker',
	'daily_effect':  'Skymall',
	'goblin_killer':  'Goblin Killer',
	'forge_time':  'Quick Forge',
	'pickaxe_toss':  'Pickobulus',
	'fallen_star_bonus':  'Crystallized',
	'experience_orbs':  'Orbiter',
	'front_loaded':  'Front Loaded',
	'precision_mining':  'Precision Mining',
	'star_powder':  'Star Powder',
	'maniac_miner':  'Maniac Miner',
	'random_event':  'Random Event',
	'special_0':  'Peak of the Mountain'
	}
mining_core_data = yes['members'][trimid].get('mining_core', {})
found_values = {value: mining_core_data['nodes'][value] for value in desired_values if 'nodes' in mining_core_data and value in mining_core_data['nodes']}

if found_values:
    print('Heart of the Mountain perks found:')
    for value, perk_value in found_values.items():
        mining_perks = perk_names.get(value, value)  # Get the custom string for the perk or use the perk name as default
        print(f'{mining_perks}: {perk_value}')
else:
    print('No Heart of the Mountain perks found!')
print('------------------------\nDungeon chests\n------------------------')
chests = yes.get('members', {}).get(trimid, {}).get('dungeons', {}).get('treasures', {}).get('chests', [])

for index, chest in enumerate(chests):
    rewards = chest.get('rewards', {}).get('rewards', [])
    if rewards:
        print(f"Chest {index + 1}:")
        for reward in rewards:
            print('    ',reward)
    else:
        print(f"No rewards found for Chest {index + 1}.")


print('------------------------\nArmor\n------------------------')

armor = yes['members'][trimid]['inv_armor']['data']
equipment = yes['members'][trimid]['equippment_contents']['data']
decode_armor = base64.b64decode(armor)
decode_equip = base64.b64decode(equipment)
gzip_armor = gzip.decompress(decode_armor)
gzip_equip = gzip.decompress(decode_equip)
armor_stream = io.BytesIO(gzip_armor)
equip_stream = io.BytesIO(gzip_equip)
arm_nbt = NBTFile(armor_stream)
equ_nbt = NBTFile(equip_stream)
arm_tree = arm_nbt.pretty()
equ_tree = equ_nbt.pretty()
print(arm_tree)
print(equ_tree)
print('------------------------\nInventory\n------------------------')
print('Searching for Necron Blade + Terminator')
inv = yes['members'][trimid]['inv_contents']['data']
decode_inv = base64.b64decode(inv)
gzip_inv = gzip.decompress(decode_inv)


stream = io.BytesIO(gzip_inv)
inv_nbt = NBTFile(stream)
inv_tree = inv_nbt.pretty()
print(inv_tree)
