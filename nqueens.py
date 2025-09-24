import random
from timeit import default_timer as timer
from collections import Counter

class Board:
    def __init__(self, board=None):
        self.board = board
        self.boardfitness = None
        self.probability = 0

    board: list
    boardfitness: int
    probability: float

global n                # Number of queens or the size of the board
global population_size  # This is the starting population size
global max_generations  # Max generations untill we stop the simulation and accept the solution we got
global mutation_rate    # Start mutation rate (will end on 1% - 5% roughly)
global elites           # How many elites we want to save into the new generation

# Generates a new random board state depending on the size N of the board with N queens.
# This gives a board state that can't have two queens on the same row or column meaning our only condition breaks
# are if the queens colide on a diagonal. Meaning the initial fitness score will be rather high (most likely).
def generate_board(N):
    return random.sample(range(N), N)


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


# Function that combines two parents (two different boards) into a child (a new board state).
def crossover(parent_1, parent_2):
    newchild = [None] * n

    i = random.randint(0, n - 2)
    j = random.randint(i + 1, n - 1)

    newchild[i:j + 1] = parent_1.board[i:j + 1]

    index = 0
    for queen in parent_2.board:
        if queen in newchild:
            continue
        while newchild[index] != None:
            index += 1
        newchild[index] = queen

    return newchild


# Function that given a board state there is a random chance to swap a queen from a random column into a new row.
def mutate(curboard):
    column1 = random.randint(0, n - 1)
    column2 = random.randint(0, n - 1)
    curboard.board[column1], curboard.board[column2] = curboard.board[column2], curboard.board[column1]
    return curboard


# Given our entire board state, we return a pair of two boards that should be used to create two new boards.
# We make sure to not pick the same board twice.
def survival_off_the_fittest(population, k=3):
    # Sista verisionen verkar vara snabbast. Blir lixom ingen vikt i valen så de går väldigt snabbt
    candidates = random.sample(population, k)
    p1 = max(candidates, key=lambda b: b.boardfitness)
    candidates = random.sample(population, k)
    p2 = max(candidates, key=lambda b: b.boardfitness)
    return p1, p2

    # Testade detta som är samma sak men inbyggd i C
    return random.choices(population, weights=[b.boardfitness for b in population], k=2)

    # Vår första lösning den suger och är för sölig
    selection_number1 = random.random()
    selection_number2 = random.random()

    p1, p2 = None, None

    for i, curboard in enumerate(population):
        if selection_number1 <= curboard.probability:
            p1 = population[i]
            break
        selection_number1 -= curboard.probability

    # Same loop but we make sure to not pick the same board again.
    for j, curboard in enumerate(population):
        if selection_number2 <= curboard.probability:
            if p1 == population[j]:
                if j > 0:
                    p2 = population[j - 1]
                else:
                    p2 = population[j + 1]
            else:
                p2 = population[j]
            break
        selection_number2 -= curboard.probability

    return p1, p2


# Function that lowers the mutation_rate untill a set lower bound rate
# OBS maybe change this to adaptive decay in the future
def mutation_rate_decay():
    global mutation_rate
    mutation_rate = max(0.05, mutation_rate * 0.99)


def fitness_probability(population):
    total_fitness = 0

    for curboard in population:
        curboard.boardfitness = fitness(curboard.board)
        total_fitness += curboard.boardfitness
    for curboard in population:
        curboard.probability = curboard.boardfitness / total_fitness

    population.sort(key=lambda x: x.boardfitness, reverse=True)



def evolutionary_algorithm():
    global n
    global population_size
    global max_generations
    global mutation_rate
    global elites

    max_fitness = n * (n - 1) // 2
    population = []

    for _ in range(population_size):
        curboard = Board()
        curboard.board = generate_board(n)
        population.append(curboard)

    for gen in range(max_generations):
        fitness_probability(population)

        if population[0].boardfitness == max_fitness:
            print(f"Max fitness has been reached! {population[0].board}")
            return True
            break

        new_population = population[:elites]

        while len(new_population) < population_size:
            p1, p2 = survival_off_the_fittest(population)
            c1 = Board(crossover(p1, p2))
            if random.random() <= mutation_rate:
                mutate(c1)

            new_population.append(c1)

        population = new_population
        mutation_rate_decay()

    return False


def main():
    global n
    global population_size
    global max_generations
    global mutation_rate
    global elites

    open("Result.txt", "w").close()

    for board_size, pop_size, generations, mutate, elite_count in parameters:
        n = board_size
        population_size = pop_size
        max_generations = generations
        mutation_rate = mutate
        elites = elite_count

        print(f"Starting simulation Using - N = {n} - pop_size = {population_size} - max_generations = {max_generations} - mutation_start_rate = {mutate} - elites = {elites}")

        total_elapsed = 0
        total_successful = 0

        for i in range(25):
            start = timer()

            if evolutionary_algorithm():
                total_successful += 1

            end = timer()

            total_elapsed += end - start
            print(f"Simuation {i + 1} finished!")

        with open("Result.txt", "a") as f:
            f.write(f"Using - N = {n} - pop_size = {population_size} - max_generations = {max_generations} - mutation_start_rate = {mutate} - elites = {elites}\n")
            f.write(f"Took a average of {total_elapsed / 25} Seconds with {total_successful} perfect runs!\n\n")

    return


# Our values that we want to test in our simulation
# It will then run 25 simulations on the given parameters and print some (pretty bad output to a file)
#            [n, population_size, max_generations, mutation_rate, elites]
parameters = [
            # Litet bräde
            [15, 50, 500, 0.2, 2],
            [15, 100, 500, 0.2, 2],
            [15, 100, 500, 0.1, 2],
            [15, 100, 500, 0.3, 2],

            # Mellan bräde
            [50, 100, 1000, 0.2, 4],
            [50, 200, 1000, 0.2, 4],

            # Stort bräde
            [100, 200, 1500, 0.2, 6],
            ]

main()