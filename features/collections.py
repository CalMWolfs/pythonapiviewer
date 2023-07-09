import json

from utils.text_utils import printSmallHeader, fmt_num


with open('constants.json') as file:
    constants = json.load(file)

highest_tiers = {}


# only the single user's count not whole coop
def getCollectionAmount(data):
    for collection_type in constants['collections']:
        printSmallHeader(collection_type)
        collections_dict = constants['collections'][collection_type]

        for collection in collections_dict:
            amount = fmt_num(data.get(collection, 0))
            display_name = collections_dict.get(collection, collection)
            print(f'{display_name} {highest_tiers.get(collection, 0)} with {amount} collected')


# saves the highest collection tier for each item. Currently no way to tell if it is maxed or not
def saveCollectionLevel(data):
    for unlocked_tier in data:
        collection, tier = unlocked_tier.rsplit('_', 1)
        if collection not in highest_tiers or int(tier) > int(highest_tiers[collection]):
            highest_tiers[collection] = tier

    for collection in highest_tiers:
        if highest_tiers.get(collection) == '-1':
            highest_tiers[collection] = '0'
