def is_safe(board, row, col, n):
   
    for i in range(row):
        if board[i] == col:
            return False
    for i in range(row):
        if abs(board[i] - col) == abs(i - row):
            return False
    
    return True


def solve_nqueens(board, row, n, solutions):
    
    if row == n:
        solutions.append(board.copy())
        print_board(board, n)
        print("solution found!")
        print("\n--------------------\n")
        return
    
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col
            print_board(board, n)
            print("\n")
            solve_nqueens(board, row + 1, n, solutions)
            board[row] = -1  


def print_board(board, n):
    for i in range(n):
        for j in range(n):
            if board[i] == j:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()


def solve_four_queens():
    n = 4
    board = [-1] * n
    solutions = []
    
    solve_nqueens(board, 0, n, solutions)
    
    print(f"Total solutions found: {len(solutions)}")
    for idx, sol in enumerate(solutions, 1):
        print(f"Solution {idx}: {sol}")


if __name__ == "__main__":
    solve_four_queens()