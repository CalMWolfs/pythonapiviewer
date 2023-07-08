import json

from utils.text_formatting import printSmallHeader, fmt_num


with open('constants.json') as file:
    constants = json.load(file)


# only the single user's count not whole coop
def getCollectionAmount(data):
    counter = 0
    output = ""

    for collection_type in constants['collections']:
        printSmallHeader(collection_type)
        collections_dict = constants['collections'][collection_type]

        for collection in collections_dict:
            amount = fmt_num(data.get(collection, 0))
            display_name = collections_dict.get(collection, collection)
            output += f'{display_name}: {amount} '
            counter += 1

            if counter % 4 == 0:
                print(output)
                output = ""

    if output:
        print(output)
