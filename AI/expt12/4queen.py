swaps=0
def is_safe(board, n):
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                return False
            if abs(board[i] - board[j]) == abs(i - j):
                return False
    return True


def swap(board, i, j):
    global swaps
    board[i], board[j] = board[j], board[i]
    swaps += 1


def solve_n_queens_swap(board, l, r, n, solutions):
    if l == r:
        if is_safe(board, n):
            solutions.append(board.copy())
            print_board(board)
            print("solution found!")
            print("\n--------------------\n")
    else:
        for i in range(l, r):
            swap(board, l, i)
            solve_n_queens_swap(board, l + 1, r, n, solutions)
            swap(board, l, i)


def print_board(board):
    n = len(board)
    for i in range(n):
        row = ""
        for j in range(n):
            if board[i] == j:
                row += "Q "
            else:
                row += ". "
        print(row)


def solve_4_queens():
    n = 4
    board = list(range(n))
    solutions = []
    
    print("Finding all solutions using Swapping approach:\n")
    solve_n_queens_swap(board, 0, n, n, solutions)
    
    print(f"\nTotal solutions found: {len(solutions)}")
    for idx, sol in enumerate(solutions, 1):
        print(f"Solution {idx}: {sol}")
    
    print(f"\nTotal swaps made: {swaps}")


if __name__ == "__main__":
    solve_4_queens()