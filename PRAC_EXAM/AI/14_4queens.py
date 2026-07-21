def is_safe(board, n):
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                return False
            if abs(board[i] - board[j]) == abs(i - j):
                return False
    return True

def solve_queens(board, l, r, n, solutions):
    if l == r:
        if is_safe(board, n):
            solutions.append(board.copy())
    else:
        for i in range(l, r):
            board[l], board[i] = board[i], board[l]
            solve_queens(board, l + 1, r, n, solutions)
            board[l], board[i] = board[i], board[l]

def print_board(board):
    for i in range(len(board)):
        row = ""
        for j in range(len(board)):
            row += "Q " if board[i] == j else ". "
        print(row)
    print()

n = 4
board = list(range(n))
solutions = []

print("4 Queens Problem\n")
solve_queens(board, 0, n, n, solutions)

print(f"Solutions found: {len(solutions)}\n")
for idx, sol in enumerate(solutions, 1):
    print(f"Solution {idx}: {sol}")
    print_board(sol)
