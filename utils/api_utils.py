import requests
import json

from secrets import API_KEY


def getPlayerUUID(player):
    uuid = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{player}')
    return uuid


def getSkyBlockData(uuid):
    data = requests.get('https://api.hypixel.net/skyblock/profiles?key=' + API_KEY + '&uuid=' + uuid)
    return data


# todo better error stuff I guess
def getPlayerData(username):
    try:
        uuid = getPlayerUUID(username)
        uuid.raise_for_status()

        player_data = getSkyBlockData(uuid.json()['id'])
        player_data.raise_for_status()

        return player_data.json().get('profiles', []), uuid.json()['id']

    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {str(e)}')
    except KeyError:
        print('Invalid username or user not found. Please try again.')
    except json.JSONDecodeError:
        print('Invalid JSON received.')


def getSoopyNetworth(player_data, uuid):
    networth_data = requests.post(f'https://soopy.dev/api/v2/player_networth/{uuid}', json=player_data)
    return networth_data.json()
