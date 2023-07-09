def selectProfile(data, uuid):
    for index, profile in enumerate(data, start=1):
        fruit = profile.get('cute_name', '')
        mode = profile.get('game_mode', 'Classic')
        level = profile.get('members', {}).get(uuid, {}).get('leveling', {}).get('experience', 0) / 100
        selected = '  Currently Selected' if profile.get('selected', '') else ''
        print(f'Profile {index}: {fruit} - {mode.capitalize()}, Level {level}{selected}')

    while True:
        user_input = input('Enter the profile number to access: ')
        entry = int(user_input) - 1

        if 0 <= entry < len(data):
            profile_data = data[entry]
            fruit = profile_data.get('cute_name', '')
            mode = profile_data.get('game_mode', 'Classic')
            print(f'Selected: {fruit} - {mode}')
            return profile_data, entry
        else:
            print('Invalid input. Please try again.')
