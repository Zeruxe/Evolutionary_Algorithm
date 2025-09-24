import random
from timeit import default_timer as timer

class Board:
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
    fitness_score = n * (n - 1) // 2

    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == j - i: # Same diagonal
                fitness_score -= 1
            elif (board[i] == board[j]): # Same row
                fitness_score -= 1
    return fitness_score


# Function that combines two parents (two different boards) into a child (a new board state).
def crossover(parent_1, parent_2, cut_off):
    return parent_1.board[:cut_off] + parent_2.board[cut_off:]


# Function that given a board state there is a random chance to swap a queen from a random column into a new row.
def mutate(curboard):
    column = random.randint(0, n - 1)
    newrow = random.randint(0, n - 1)
    curboard.board[column] = newrow
    return curboard


# Given our entire board state, we return a pair of two boards that should be used to create two new boards.
# We make sure to not pick the same board twice.
def survival_off_the_fittest(population):
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
    if mutation_rate > 0.01:
        mutation_rate -= 0.01


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

    start = timer()

    max_fitness = n * (n - 1) // 2
    population = []

    for _ in range(population_size):
        curboard = Board()
        curboard.board = generate_board(n)
        population.append(curboard)

    for gen in range(max_generations):
        fitness_probability(population)

        print(max_fitness, population[0].boardfitness, population[0].board)

        if population[0].boardfitness == max_fitness:
            print(f"Max fitness has been reached! {population[0].board}")
            break

        new_population = population[:elites]

        while len(new_population) < population_size:
            p1, p2 = survival_off_the_fittest(population)
            cutoff = random.randint(1, n - 1)
            c1 = Board()
            c1.board = crossover(p1, p2, cutoff)
            if random.random() <= mutation_rate:
                c1 = mutate(c1)

            new_population.append(c1)

            c2 = Board()
            c2.board = crossover(p2, p1, cutoff)
            if random.random() <= mutation_rate:
                c2 = mutate(c2)
            new_population.append(c2)

        print("Before", len(population))
        for pop in population:
            print(pop.board, pop.boardfitness)
        population = new_population
        print("After", len(population))
        for pop in population:
            print(pop.board)

        mutation_rate_decay()

        if gen == 2:
            return 1

    end = timer()
    return end - start


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

        total_elapsed = 0

        print(f"Starting simulation Using - N = {n} - pop_size = {population_size} - max_generations = {max_generations} - mutation_start_rate = {mutate} - elites = {elites}")

        for i in range(5):
            total_elapsed += evolutionary_algorithm()
            print(f"Simuation {i + 1} finished!")

        with open("Result.txt", "a") as f:
            f.write(f"Using - N = {n} - pop_size = {population_size} - max_generations = {max_generations} - mutation_start_rate = {mutate} - elites = {elites}\n")
            f.write(f"Took a average of {total_elapsed / 5} Seconds\n\n")

    return


# Our values that we want to test in our simulation
# It will then run 25 simulations on the given parameters and print some (pretty bad output to a file)
#            [n, population_size, max_generations, mutation_rate, elites]
parameters = [[8, 6, 5000, 0.1, 2]
              #[8, 100, 5000, 0.2, 10], 
              #[8, 250, 5000, 0.2, 10],
              #[8, 500, 5000, 0.2, 10],
              #[8, 1000, 5000, 0.2, 10],
              #[8, 2000, 5000, 0.2, 10],
              #[8, 5000, 5000, 0.2, 10],
              #[8, 10000, 5000, 0.2, 10]
              ]

if __name__ == "__main__": 
    main()