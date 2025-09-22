import random

class Board:
    board: list
    boardfitness: int
    probability: float

n = 8                   # Number of queens or the size of the board
population_size = 100   # This is the starting population size
max_generations = 5000  # Max generations untill we stop the simulation and accept the solution we got
mutation_rate = 0.20    # Start mutation rate (will end on 1% - 5% roughly)
elites = 2              # How many elites we want to save into the new generation

# Generates a new random board state depending on the size N of the board with N queens.
# This gives a board state that can't have two queens on the same row or column meaning our only condition breaks
# are if the queens colide on a diagonal. Meaning the initial fitness score will be rather high (most likely).
def generate_board(N):
    return random.Shuffle([x for x in range(N)])


# A function that given one of our boards. It returns the current fitness_score of that board.
# The fitness score is how many queens that do not conflict with eachother.
def fitness(board):
    fitness_score = n * (n - 1) // 2

    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == j - i: # Same diagonal
                fitness_score -= 1
            elif (i == board[j]): # Same row
                fitness_score -= 1
            elif (board[i] == j): # Same Column
                fitness_score -= 1
    return fitness_score


# Function that combines two parents (two different boards) into a child (a new board state).
def crossover(parent_1, parent_2, cut_off):
    return parent_1[:cut_off] + parent_2[cut_off:]


# Function that given a board state there is a random chance to swap a queen from a random column into a new row.
def mutate(board):
    if random.random() < mutation_rate:
        column = random.randint(n)
        newrow = random.randint(n)
        board[column] = newrow
    return board


# Given our entire board state, we return a pair of two boards that should be used to create two new boards.
# We make sure to not pick the same board twice.
def survival_off_the_fittest(population):
    selection_number1 = random.random()
    selection_number2 = random.random()

    p1, p1 = None, None

    for i, probability in enumerate(population):
        if selection_number1 <= population.probability:
            p1 = population[i]
            break
        selection_number1 -= probability

    # Same loop but we make sure to not pick the same board again.
    for j, probability in enumerate(population):
        if selection_number2 <= population.probability:
            if p1 == population[j]:
                if j > 0:
                    p2 = population[j - 1]
                else:
                    p2 = population[j + 1]
            else:
                p2 = population[j]
            break
        selection_number2 -= population.probability

    return (p1, p2)


# Function that lowers the mutation_rate untill a set lower bound rate
def mutation_rate_decay():
    if mutation_rate > 0.01:
        mutation_rate -= 0.01


def fitness_probability(population):
    total_fitness = 0

    for curboard in population:
        curboard.boardfitness = fitness(curboard.board)
        total_fitness += curboard.boardfitness
    for curboard in population:
        current_probability = curboard.boardfitness / total_fitness

    population.sort(key=population.boardfitness, reverse=True)


def main():

    return