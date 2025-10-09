from timeit import default_timer as timer
from evolutionary_algorithm import evolutionary_algorithm


# Our values that we want to test in our simulation
# It will then run 25 simulations on the given parameters and print some (pretty bad output to a file)
#            [n, population_size, max_generations, mutation_rate, elites]
parameters = [
            # Små Bräden
            [10, 20, 200, 0.2, 1],
            [20, 40, 225, 0.2, 1],
            [30, 60, 250, 0.2, 1],
            [40, 80, 275, 0.2, 1],
            [50, 100, 300, 0.2, 1],

            #[10, 400, 250, 0.3, 2],
            #[15, 400, 250, 0.3, 2],
            #[20, 400, 250, 0.3, 2],
            #[25, 400, 250, 0.3, 2],

            # Mellanstora Bräden
            #[30, 400, 250, 0.3, 2],
            #[35, 400, 250, 0.3, 2],
            #[40, 400, 250, 0.3, 2],
            #[45, 400, 250, 0.3, 2],
            #[50, 400, 250, 0.3, 2],

            # Stora Bräden
            #[100, 400, 250, 0.3, 2],
            #[250, 600, 1000, 0.3, 2],
            #[500, 800, 1000, 0.3, 2]
            ]


def main():
    open("Results/Evolutionary_Algorithm.txt", "w").close()
    open("Results/PlotEvolutionary_Algorithm.txt", "w").close()

    for n, population_size, max_generations, mutation_rate, elites_count in parameters:
        total_elapsed = 0
        total_successful = 0

        for i in range(10):
            start = timer()

            if evolutionary_algorithm(n, population_size, max_generations, mutation_rate, elites_count):
                total_successful += 1

            end = timer()

            total_elapsed += end - start
            print(f"Simuation {i + 1} finished!")

        with open("Results/Evolutionary_Algorithm.txt", "a") as f:
            f.write(f"Using - N = {n} - pop_size = {population_size} - max_generations = {max_generations} - mutation_start_rate = {mutation_rate} - elites = {elites_count}\n")
            f.write(f"Took a average of {total_elapsed / 10} Seconds with {total_successful} perfect runs!\n\n")

        with open("Results/PlotEvolutionary_Algorithm.txt", "a") as f:
            f.write(f"{n}\n")
            f.write(f"{total_elapsed/10}\n")

def GetBestParametersForN(n):
    p_size = list(range(10, 101, 10)) + list(range(150, 501, 50))
    max_gens = list(range(100, 501, 100)) + list(range(1000, 2001, 500))

    best_p_size = 0
    best_gens = 0

    min_time = float('inf')

    for gen in max_gens:
        for p in p_size:
            total_completed = 0
            start = timer()
            for i in range(30):
                if evolutionary_algorithm(n, p, gen, 0.2, p // 10):
                    total_completed += 1

            end = timer()

            if total_completed >= 27 and end - start <= min_time:
                min_time = end - start
                best_p_size = p
                best_gens = gen

    print(f"For N = {n} our best parameters were: Population_Size = {best_p_size} and Max_Generations = {best_gens}")


# Byt mellan dessa main() är vanliga grejen och den andra testar massa parametrar.
main()
