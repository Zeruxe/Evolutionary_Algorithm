import random
from board_state import generate_board, crossover, mutate
from fitness import population_fitness_sort, fitness
from selection import survival_off_the_fittest

class Board:
    def __init__(self, board=None):
        self.board = board
        self.boardfitness = None
        self.probability = 0

    board: list
    boardfitness: int
    probability: float


def evolutionary_algorithm(n, population_size, max_generations, mutation_rate, elites):
    max_fitness = n * (n - 1) // 2
    population = []

    last_best_fitness = -1
    gens_since_improvement = 0

    for _ in range(population_size):
        curboard = Board()
        curboard.board = generate_board(n)
        population.append(curboard)

    for gen in range(max_generations):
        population_fitness_sort(population)

        if population[0].boardfitness == max_fitness:
            print(f"Max fitness has been reached! {population[0].board}")
            return True
            
        if gens_since_improvement >= 25:
            mutation_rate = mutation_rate_increase(mutation_rate)
            gens_since_improvement = 0
            create_freshboards(n, population, population_size)

        if last_best_fitness != population[0].boardfitness:
            gens_since_improvement = 0
        else:
            gens_since_improvement += 1
        last_best_fitness = population[0].boardfitness

        new_population = population[:elites]

        while len(new_population) < population_size:
            p1, p2 = survival_off_the_fittest(population)
            c1 = Board(crossover(p1, p2, n))
            c2 = Board(crossover(p2, p1, n))
            if random.random() <= mutation_rate:
                mutate(c1, n)
            if random.random() <= mutation_rate:
                mutate(c2, n)

            new_population.append(c1)
            new_population.append(c2)

        population = new_population
        mutation_rate = mutation_rate_decay(mutation_rate)

    return False


def create_freshboards(n, population, population_size):
    newboards = []
    newboardnumber = max(1, population_size // 10)
    for _ in range(newboardnumber):
        curboard = Board()
        curboard.board = generate_board(n)
        newboards.append(curboard)
    
    for curboard in newboards:
        curboard.boardfitness = fitness(curboard.board)

    population[-newboardnumber:] = newboards



# Function that lowers the mutation_rate untill a set lower bound rate.
def mutation_rate_decay(mutation_rate):
    return max(0.05, mutation_rate * 0.99)


# Function that increases the mutation_rate up to a maximum of 0.3.
def mutation_rate_increase(mutation_rate):
    return min(mutation_rate * 2, 0.3)