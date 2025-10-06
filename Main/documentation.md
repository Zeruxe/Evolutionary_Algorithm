# N-Queens Genetic Algorithm Functions

## `generate_board(n)`
Creates a list of numbers from `0` to `n-1`, where each number represents the row position of a queen in that column.  
The list is then shuffled randomly so no two queens are in the same row or column.

---

## `crossover(p1, p2, n)`
Creates a new child board by mixing parts of two parent boards (`p1` and `p2`):

1. Picks a random slice from index `i` to `j` from parent 1.
2. Copies that slice into the new child.
3. Fills the rest of the empty spots using parent 2's queens, skipping duplicates.

This produces a child board that combines traits from both parents.

---

## `mutate(curboard, n)`
Randomly swaps two queens on the board to create a small change (mutation):

1. Picks two random columns.
2. Swaps the row positions of the queens in these columns.

This adds variation and prevents the algorithm from getting stuck on one solution.

---

## `evolutionary_algorithm(n, population_size, max_generations, mutation_rate, elites)`
Runs the genetic algorithm to find a perfect N-Queens solution:

1. Generates an initial population of random boards.
2. Sorts boards by fitness (how many queens do not attack each other).
3. If the best board is perfect, stops.
4. If the population hasn’t improved for a while, shakes things up by:
   - Adding random boards.
   - Increasing the mutation rate.
5. For the next generation:
   - Keeps the best boards (elites).
   - Selects parents using `survival_off_the_fittest`.
   - Creates children via `crossover`.
   - Applies `mutate` randomly.
6. Gradually decays the mutation rate over generations.

This continues until a perfect solution is found or the maximum number of generations is reached.

---

## `create_freshboards(n, population, population_size)`
Adds new random boards to avoid stagnation:

1. Creates a few new boards (~10% of population).
2. Calculates their fitness.
3. Replaces the worst boards in the population with these fresh boards.

This helps the algorithm explore new solutions.

---

## `mutation_rate_decay(mutation_rate)`
Gradually reduces the mutation rate over time:

- Multiplies current rate by `0.99`.
- Never lets it go below `0.05`.

Early on, high mutation allows exploration. Later, low mutation stabilizes solutions.

---

## `mutation_rate_increase(mutation_rate)`
Increases the mutation rate when stuck:

- Doubles the current rate, up to a maximum of `0.3`.

This helps the population "mix things up" and escape local traps.

---

## `population_fitness_sort(population)`
Evaluates and sorts boards by fitness:

1. Calculates the fitness of each board using `fitness()`.
2. Sorts the population from best (highest fitness) to worst.

Makes it easy to select the strongest boards for the next generation.

---

## `fitness(board)`
Measures how good a board is:

1. Starts with the maximum possible score (no queens attacking each other).
2. Checks each diagonal for conflicts.
3. Each conflict reduces the score.

Higher fitness means fewer attacks; a perfect board gets the maximum score.

---

## `survival_off_the_fittest(population, k=3)`
Selects parents for crossover:

1. Randomly chooses a small group of boards (2 × k).
2. Sorts the group by fitness.
3. Returns the two best boards as parents.

Ensures the fittest candidates reproduce while maintaining diversity.
