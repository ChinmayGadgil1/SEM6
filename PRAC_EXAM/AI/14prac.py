def is_safe(board):
    for i in range(4):
        for j in range(i+1,n):
            if board[i]==board[j]:
                return False
            if abs(board[i]-board[j])==abs(i-j):
                return False

    return True

def nqueens(board,l,r,n,solutions):
    if l==r:
        if is_safe(board):
            solutions.append(board.copy())
    else:
        for i in range(l,r):
            board[i],board[l]=board[l],board[i]
            nqueens(board,l+1,r,n,solutions)    
            board[i],board[l]=board[l],board[i]

n=4
board=list(range(n))
solutions=[]
nqueens(board,0,n,n,solutions)

for row in solutions:
    print(row)