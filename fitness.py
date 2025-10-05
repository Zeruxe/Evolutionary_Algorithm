from collections import Counter

def population_fitness_sort(population):
    for curboard in population:
        curboard.boardfitness = fitness(curboard.board)

    population.sort(key=lambda x: x.boardfitness, reverse=True)


# A function that given one of our boards. It returns the current fitness_score of that board.
# The fitness score is how many queens that do not conflict with eachother.
def fitness(board):
    n = len(board)
    max_fitness = n * (n - 1) // 2

    diag1 = Counter()
    diag2 = Counter()

    for col, row in enumerate(board):
        diag1[row - col] += 1
        diag2[row + col] += 1

    for v in diag1.values():
        max_fitness -= v * (v - 1) // 2
    for v in diag2.values():
        max_fitness -= v * (v - 1) // 2

    return max_fitness