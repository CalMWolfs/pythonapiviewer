from utils.text_utils import fmt_num, fmt_str
from utils.api_utils import getSoopyNetworthData


def getBank(data):
    print('Bank:', fmt_num(data.get('banking', {}).get('balance', 0)))


def getPurse(data):
    print('Purse:', fmt_num(data.get('coin_purse', 0)))


def getSoopyNetworth(data, uuid, profile_id):
    stripped_id = profile_id.replace('-', '')
    networth_data = getSoopyNetworthData(data, uuid)
    profile_networth = networth_data.get(stripped_id, {})

    total_networth = profile_networth.get('total', 0)
    print('Total Networth:', fmt_num(total_networth))

    categorical_networth = profile_networth.get('categories', {})
    for category in categorical_networth:
        amount = (categorical_networth.get(category, 0))
        print(f'{fmt_str(category)}: {fmt_num(amount)}')
