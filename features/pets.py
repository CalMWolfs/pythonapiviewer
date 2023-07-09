import json

import constants_parsing
from utils.text_formatting import printSmallHeader


with open('constants.json') as file:
    constants = json.load(file)


# todo more stats like unique pets or something
def getGeneralPetData(data):
    pet_score = data.get('leveling', {}).get('highest_pet_score', 0)
    printSmallHeader('Pet Stats')
    print('Highest Pet Score:', pet_score)


# todo pet items and improve the printed message in console
def getImportantPets(data):
    for pet in data:
        pet_name = pet.get('type', 0)
        pet_rarity = pet.get('tier', '')

        if pet_name in constants['important_items']['pets']:
            if pet_rarity in constants['important_items']['pets'].get(pet_name):
                pet_exp = pet.get('exp', 0)

                if pet.get('type', '') == 'GOLDEN_DRAGON':
                    level, exp = constants_parsing.getGoldenDragLevel(pet_exp)
                else:
                    level, exp = constants_parsing.getPetLevel(pet_rarity, pet_exp)
                print(pet_rarity, pet.get('type', ''), f'lvl {level} with {exp} exp')
