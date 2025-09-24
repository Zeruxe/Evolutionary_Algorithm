import random
import nqueens

backtracking_limit = 1000000
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



def main():

    n = int(input())

    new_board = nqueens.Board()
    new_board.board = [-1 for i in range(n)]

    if (placequeens(0, new_board.board)):
        print(new_board.board)
    else:
        print("No Solution found within backtracking limit")
        print("Final board state:")
        print(new_board.board)




if __name__ == "__main__":
    main()

