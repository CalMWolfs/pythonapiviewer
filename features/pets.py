import json

import constants_parsing
from utils.text_utils import printSmallHeader, fmt_str


with open('constants.json') as file:
    constants = json.load(file)


# todo more stats like unique pets or something
def getGeneralPetData(data):
    pet_score = data.get('leveling', {}).get('highest_pet_score', 0)
    printSmallHeader('Pet Stats')
    print('Highest Pet Score:', pet_score)


# todo pet items and maybe split pets by type so can display their stats better?
def getImportantPets(data):
    for pet in data:
        pet_name = pet.get('type', 0)
        pet_rarity = pet.get('tier', '')

        if pet_name in constants['important_items']['pets']:
            if pet_rarity in constants['important_items']['pets'].get(pet_name):
                pet_exp = pet.get('exp', 0)

                if pet.get('type', '') == 'GOLDEN_DRAGON':
                    pet_lvl, pet_exp = constants_parsing.getGoldenDragLevel(pet_exp)
                else:
                    pet_lvl, pet_exp = constants_parsing.getPetLevel(pet_rarity, pet_exp)
                pet_name = fmt_str(pet_name)
                print(f'Level {pet_lvl} {pet_rarity.capitalize()} {pet_name} with {pet_exp} total experience')
