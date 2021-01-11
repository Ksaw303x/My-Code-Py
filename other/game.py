def check_moves(in_move):
    x_move = 0
    y_move = 0

    if len(in_move) > 10:
        return False

    for el in in_move:
        x_move += 1 if el == 'n' else 0
        x_move -= 1 if el == 's' else 0
        y_move += 1 if el == 'e' else 0
        y_move -= 1 if el == 'o' else 0

    if x_move is 0 and y_move is 0:
        return True
    else:
        return False


if __name__ == '__main__':

    t = ['n','s','n','s','n','s','n','s','n','s']
    f = ['w','e','w','e','w','e','w','e','w','e','w','e']

    print(check_moves(t))
    print(check_moves(f))
