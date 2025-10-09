import random
from evolutionary_algorithm import Board
from timeit import default_timer as timer
from collections import Counter

backtracking_limit = 10000000
current_backtracks = 0

##Check if it's safe to place a queen at board[col] = row
def safe_place(board, col, row):
    n = len(board)


    ##Check for every column if there is a queen in the same row or diagonal
    for i in range(col):
        if board[i] == row or abs(board[i] - row) == abs(i - col):
            return False
    return True
        
##Recursive function to place all queens on the board
##If a certain spot is not valid, it backtracks and tries a different spot
def placequeens(col, board):
    n = len(board)
    
    global current_backtracks
    global backtracking_limit

    if col == n:
        return True
    
    for i in range(n):

        if (safe_place(board, col, i)):
            board[col] = i
            if (placequeens(col + 1, board)):
                return True
            board[col] = -1
            current_backtracks += 1
            if current_backtracks > backtracking_limit:
                print("Backtracking limit reached")
                print("Final board state:")
                print(board)
                return False

    return False


def backtrack_alg(n):

    global current_backtracks
    current_backtracks = 0

    print(f"Calling backtrack_alg with n={n}")  # Debug print
    new_board = Board()
    new_board.board = [-1 for i in range(n)]

    if (placequeens(0, new_board.board)):
        print(new_board.board)
        return True
    else:
        print("No Solution found within backtracking limit")
        print("Final board state:")
        print(new_board.board)
        return False


def main():

    # Try different problemsizes n
    parameters = list(range(5, 26))

    open("Results/PlotBackTracking.txt", "w").close()   

    time_elapsed = 0 

    for n in parameters:
        total_succesull = 0
        for i in range(3):     #Run 25 simulations on every n
            start = timer()
            if (backtrack_alg(n)):
                total_succesull += 1
            
            end = timer()
            time_elapsed += end - start
        
        with open("Results/PlotBackTracking.txt", "a") as f:
            ##f.write(f"Using - N = {n}\n")
            ##f.write(f"Took an average of {time_elapsed / 25} seconds with {total_succesull} perfect runs!\n\n")
            f.write(f"{n}\n")
            f.write(f"{time_elapsed/3}\n")

        
    return




if __name__ == "__main__":
    main()

