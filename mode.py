def mode_choice(mode):
    if mode == 'easy':
        return [2,3,5]
    elif mode == 'normal':
        return [2,3,5,7]
    elif mode == 'hard':
        return [2,3,5,7,11,13]
    elif mode == 'expert':
        return [2,3,5,7,11,13,17,19,23]
    elif mode == 'insane':
        return [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]