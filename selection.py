import random

# Given our entire board state, we return a pair of two boards that should be used to create two new boards.
# We make sure to not pick the same board twice.
def survival_off_the_fittest(population, k=3):
    candidates = random.sample(population, min(2 * k, len(population)))

    candidates.sort(key=lambda x: x.boardfitness, reverse=True)

    return candidates[0], candidates[1]