import random

# Generates a new random board state depending on the size N of the board with N queens.
# This gives a board state that can't have two queens on the same row or column meaning our only condition breaks
# are if the queens colide on a diagonal. Meaning the initial fitness score will be rather high (most likely).
def generate_board(n):
    return random.sample(range(n), n)


# Function that combines two parents (two different boards) into a child (a new board state).
def crossover(p1, p2, n):
    newchild = [None] * n

    i = random.randint(0, n - 2)
    j = random.randint(i + 1, n - 1)

    newchild[i:j + 1] = p1.board[i:j + 1]

    index = 0
    for queen in p2.board:
        if queen in newchild:
            continue
        while newchild[index] != None:
            index += 1
        newchild[index] = queen

    return newchild


# Function that given a board state returns a new board state that swaps two columns.
def mutate(curboard, n):
    column1 = random.randint(0, n - 1)
    column2 = random.randint(0, n - 1)

    while column1 == column2:
        column2 = random.randint(0, n - 1)

    curboard.board[column1], curboard.board[column2] = curboard.board[column2], curboard.board[column1]
    return curboard