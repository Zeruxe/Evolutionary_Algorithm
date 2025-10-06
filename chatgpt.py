import random

# ----- Parameters -----
N = 12               # number of queens
POP_SIZE = 80       # population size
MAX_GEN = 5000       # max generations
MUT_RATE = 0.8       # mutation probability
ELITISM = 4          # how many elites to keep each generation

# ----- Fitness -----
def fitness(board):
    """Fitness = number of non-attacking pairs (max possible is n*(n-1)/2)."""
    n = len(board)
    max_pairs = n * (n - 1) // 2
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(board[i] - board[j]) == j - i:  
                conflicts += 1
    return max_pairs - conflicts

# ----- Initialization -----
def random_board(n):
    """Generate a random permutation of 0..n-1 (one queen per column)."""
    board = list(range(n))
    random.shuffle(board)
    return board

# ----- Genetic operators -----
def crossover(p1, p2):
    """Order crossover (OX) for permutations."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b] = p1[a:b]
    pos = b
    for x in p2:
        if x not in child:
            if pos >= n: pos = 0
            child[pos] = x
            pos += 1
    return child

def mutate(board):
    """Swap mutation."""
    a, b = random.sample(range(len(board)), 2)
    board[a], board[b] = board[b], board[a]

# ----- Selection -----
def tournament(pop, k=3):
    """Tournament selection: pick k random, return best."""
    best = random.choice(pop)
    for _ in range(k - 1):
        contender = random.choice(pop)
        if fitness(contender) > fitness(best):
            best = contender
    return best

# ----- Main GA loop -----
def genetic_algorithm():
    pop = [random_board(N) for _ in range(POP_SIZE)]
    max_pairs = N * (N - 1) // 2

    for gen in range(MAX_GEN):
        pop.sort(key=fitness, reverse=True)
        best = pop[0]

        # 🔹 Print progress
        print(f"Generation {gen}, Best fitness = {fitness(best)}")

        if fitness(best) == max_pairs:
            print(f"✅ Solution found in {gen} generations!")
            return best

        new_pop = pop[:ELITISM]  # elitism
        while len(new_pop) < POP_SIZE:
            p1, p2 = tournament(pop), tournament(pop)
            child = crossover(p1, p2)
            if random.random() < MUT_RATE:
                mutate(child)
            new_pop.append(child)
        pop = new_pop

    print("⚠️ No perfect solution found (reached MAX_GEN).")
    return pop[0]

solution = genetic_algorithm()
print("Best board:", solution)
print("Fitness:", fitness(solution))

