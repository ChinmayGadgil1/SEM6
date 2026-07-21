board = [['_' for _ in range(3)] for _ in range(3)]

def print_board():
    for row in board:
        print(" ".join(row))
    print()

def check_win(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full():
    return all(cell != '_' for row in board for cell in row)

def minimax(is_max):
    if check_win('O'):
        return 10
    if check_win('X'):
        return -10
    if is_full():
        return 0
    
    if is_max:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'O'
                    best = max(best, minimax(False))
                    board[i][j] = '_'
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'X'
                    best = min(best, minimax(True))
                    board[i][j] = '_'
        return best

def best_move():
    best_score = -1000
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'O'
                score = minimax(False)
                board[i][j] = '_'
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def play():
    print_board()
    while True:
        r, c = map(int, input("Your move (row col): ").split())
        if board[r][c] == '_':
            board[r][c] = 'X'
            print_board()
            
            if check_win('X'):
                print("You win!")
                break
            if is_full():
                print("Draw!")
                break
            
            move = best_move()
            board[move[0]][move[1]] = 'O'
            print("Computer's move:")
            print_board()
            
            if check_win('O'):
                print("Computer wins!")
                break
            if is_full():
                print("Draw!")
                break

play()
