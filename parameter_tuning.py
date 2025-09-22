from evolutionary_algorithm import EvolutionaryAlgorithm
from main import fitness, random_board, crossover, mutate
import random

def tune_parameters():
    """Example of parameter tuning using the base implementation."""
    
    N = 8  # Smaller problem for faster tuning
    max_pairs = N * (N - 1) // 2
    
    # Parameter combinations to test
    param_combinations = [
        {'population_size': 50, 'mutation_rate': 0.1, 'elitism_count': 2},
        {'population_size': 100, 'mutation_rate': 0.3, 'elitism_count': 5},
        {'population_size': 80, 'mutation_rate': 0.8, 'elitism_count': 4},
    ]
    
    best_params = None
    best_avg_fitness = 0
    
    for params in param_combinations:
        print(f"\nTesting parameters: {params}")
        
        total_fitness = 0
        runs = 5
        
        for run in range(runs):
            ea = EvolutionaryAlgorithm(
                max_generations=1000,
                **params
            )
            
            ea.set_problem_functions(
                fitness_func=fitness,
                crossover_func=crossover,
                mutation_func=mutate,
                init_func=lambda: random_board()  # Adapted for N=8
            )
            
            solution, _ = ea.evolve(target_fitness=max_pairs, verbose=False)
            total_fitness += fitness(solution)
        
        avg_fitness = total_fitness / runs
        print(f"Average fitness over {runs} runs: {avg_fitness:.2f}")
        
        if avg_fitness > best_avg_fitness:
            best_avg_fitness = avg_fitness
            best_params = params
    
    print(f"\nBest parameters: {best_params}")
    print(f"Best average fitness: {best_avg_fitness:.2f}")

if __name__ == "__main__":
    tune_parameters()
