def getSkyblockLevel(data):
    skyblock_level = data.get('leveling', {}).get('experience', 0) / 100
    print(f'SkyBlock level: {skyblock_level}')
