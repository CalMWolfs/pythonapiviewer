from utils.text_utils import fmt_num
from utils.api_utils import getPlayerData, getMuseumData
from utils.player_selection import selectProfile

username = input('Username: ')
player_data, uuid = getPlayerData(username)

profile_data, profile_num = selectProfile(player_data, uuid)

profile_specific = profile_data['members'][uuid]
profile_id = player_data[profile_num].get('profile_id', '')

museum_data = getMuseumData(profile_id).json()

player_specific_museum = museum_data.get('members', {}).get(uuid, {})
value = player_specific_museum.get('value', 0)
print(fmt_num(value))
