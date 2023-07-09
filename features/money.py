from utils.text_utils import fmt_num


def getBank(data):
    print('Bank:', fmt_num(data.get('banking', {}).get('balance', 0)))


def getPurse(data):
    print('Purse:', fmt_num(data.get('coin_purse', 0)))
