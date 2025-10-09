from timeit import default_timer as timer
from evolutionary_algorithm import evolutionary_algorithm
from evolutionary_algorithm import get_all_solutions, clear_best_board

# Our values that we want to test in our simulation
# It will then run 25 simulations on the given parameters and print some (pretty bad output to a file)
#            [n, population_size, max_generations, mutation_rate, elites]
#parameters = [5, 10, 25, 50, 100, 250, 500, 1000]
parameters = [5, 10, 25, 50, 100, 125, 150, 175, 200]
def main():
    open("../Results/Evolutionary_Algorithm.txt", "w").close()
    open("../Results/PlotEvolutionary_Algorithm.txt", "w").close()
    open("../Results/All_solutions.txt", "w").close()

    for n in parameters:
        total_elapsed = 0
        total_successful = 0

        for i in range(25):
            start = timer()

            if evolutionary_algorithm(n):
                total_successful += 1

            end = timer()

            total_elapsed += end - start
            print(f"Simuation {i + 1} finished! It took {end - start} seconds")




        solutions = get_all_solutions()

        with open("../Results/All_solutions.txt", "a") as f:
            f.write(f"N = {n}\n")
            f.write(f"Max fittness: {n * (n - 1) // 2}\n")
            f.write(f" All solutions: {solutions}\n\n")

        clear_best_board()

        with open("../Results/Evolutionary_Algorithm.txt", "a") as f:
            f.write(f"N = {n}\n")
            f.write(f"Took a average of {total_elapsed / 25} Seconds with {total_successful} perfect runs!\n\n")
            
        with open("../Results/PlotEvolutionary_Algorithm.txt", "a") as f:
            f.write(f"{n}\n")
            f.write(f"{total_elapsed/25}\n")


main()