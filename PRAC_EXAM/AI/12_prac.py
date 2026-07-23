board=[['_' for _ in range(3)] for _ in range(3)]

def isFull():
    for row in board:
        for e in row:
            if e=='_':
                return False
    return True

def check_win(player):
    for row in board:
        all_player=True
        for e in row:
            if e !=player:
                all_player=False
                break
        if all_player==True:
            return True

    for col in range(3):
        all_player=True
        for row in range(3):
            if board[row][col]!=player:
                all_player=False
                break
        if all_player==True:
            return True
        
    all_player=True
    for i in range(3):
        if board[i][i]!=player:
            all_player=False
            break
    if all_player==True:
        return True
    all_player=True
    for i in range(3):
        if board[i][2-i]!=player:
            all_player=False
            break
        
    if all_player==True:
        return True
    else:
        return False
            

def minimax(player):
    if check_win('X'):
        return -10
    if check_win('O'):
        return 10
    if isFull():
        return 0
    
    if player==True:
        best=-1000
        for i in range(3):
            for j in range(3):
                if board[i][j]=='_':
                    board[i][j]='O'
                    best=max(best,minimax(False))
                    board[i][j]='_'
        return best
    if player==False:
        best=1000
        for i in range(3):
            for j in range(3):
                if board[i][j]=='_':
                    board[i][j]='X'
                    best=min(best,minimax(True))
                    board[i][j]='_'
        return best                 
        
def best_move():
    best=-1000
    move=None
    for i in range(3):
        for j in range(3):
            if board[i][j]=='_':
                board[i][j]='O'
                score=minimax(False)
                board[i][j]='_'
                if score>best:
                    best=score
                    move=(i,j)
    return move

def printboard():
    for row in board:
        for e in row:
            print(e,end=' ')
        print()

def play():
    while True:
        r=int(input("Enter row:"))
        c=int(input("Enter col:"))
        
        if board[r][c]!='_':
            continue
        
        board[r][c]='X'
        printboard()
        if check_win('X'):
            print("X win")
            return
        if isFull():
            print("Draw")
            return
        
        move=best_move()
        board[move[0]][move[1]]='O'
        
        if check_win('O'):
            print("O win")
            return
        if isFull():
            print("Draw")
            return
        printboard()
        
play()