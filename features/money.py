from utils.text_formatting import fmt_num


def printBank(data):
    print('Bank:', fmt_num(data.get('banking', {}).get('balance', 0)))


def printPurse(data):
    print('Purse:', fmt_num(data.get('coin_purse', 0)))
