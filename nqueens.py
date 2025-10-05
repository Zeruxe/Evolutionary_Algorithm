from timeit import default_timer as timer
from evolutionary_algorithm import evolutionary_algorithm


# Our values that we want to test in our simulation
# It will then run 25 simulations on the given parameters and print some (pretty bad output to a file)
#            [n, population_size, max_generations, mutation_rate, elites]
parameters = [
            # Små Bräden
            [5, 50, 500, 0.3, 2],
            [10, 100, 1000, 0.3, 2],
            [15, 100, 1500, 0.3, 2],
            [20, 100, 1500, 0.3, 2],
            [25, 200, 2000, 0.3, 2],

            # Mellanstora Bräden
            [30, 250, 2000, 0.3, 2],
            [35, 300, 2000, 0.3, 2],
            [40, 350, 2000, 0.3, 2],
            [45, 400, 2000, 0.3, 2],
            [50, 450, 2000, 0.3, 2],

            # Stora Bräden
            #[100, 500, 4000, 0.3, 2],
            #[250, 600, 4000, 0.3, 2],
            #[500, 800, 4000, 0.3, 2]
            ]


open("Results/Evolutionary_Algorithm.txt", "w").close()
open("Results/PlotEvolutionary_Algorithm.txt", "w").close()

for n, population_size, max_generations, mutation_rate, elites_count in parameters:
    total_elapsed = 0
    total_successful = 0

    for i in range(25):
        start = timer()

        if evolutionary_algorithm(n, population_size, max_generations, mutation_rate, elites_count):
            total_successful += 1

        end = timer()

        total_elapsed += end - start
        print(f"Simuation {i + 1} finished!")

    with open("Results/Evolutionary_Algorithm.txt", "a") as f:
        f.write(f"Using - N = {n} - pop_size = {population_size} - max_generations = {max_generations} - mutation_start_rate = {mutation_rate} - elites = {elites_count}\n")
        f.write(f"Took a average of {total_elapsed / 25} Seconds with {total_successful} perfect runs!\n\n")

    with open("Results/PlotEvolutionary_Algorithm.txt", "a") as f:
        f.write(f"{n}\n")
        f.write(f"{total_elapsed/25}\n")