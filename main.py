from evolutionary_algorithm import EvolutionaryAlgorithm
import random

# ----- N-Queens Problem Implementation -----
N = 12  # number of queens

def fitness(board):
    """
    Fitness function for N-Queens problem.
    Fitness = number of non-attacking pairs (max possible is n*(n-1)/2).
    Higher fitness is better.
    """
    n = len(board)
    max_pairs = n * (n - 1) // 2
    conflicts = 0
    
    # Count diagonal conflicts
    for i in range(n):
        for j in range(i + 1, n):
            # Check if queens are on same diagonal
            if abs(board[i] - board[j]) == j - i:  
                conflicts += 1
    
    return max_pairs - conflicts

def random_board():
    """
    Generate a random permutation of 0..n-1 (one queen per column).
    Each number represents the row position of queen in that column.
    """
    board = list(range(N))
    random.shuffle(board)
    return board

def crossover(parent1, parent2):
    """
    Order crossover (OX) for permutations.
    Preserves the order and position information from both parents.
    """
    n = len(parent1)
    # Select two random crossover points
    a, b = sorted(random.sample(range(n), 2))
    
    # Initialize child with None values
    child = [None] * n
    
    # Copy segment from parent1
    child[a:b] = parent1[a:b]
    
    # Fill remaining positions with elements from parent2 in order
    pos = b
    for element in parent2:
        if element not in child:
            if pos >= n:
                pos = 0
            child[pos] = element
            pos += 1
    
    return child

def mutate(board):
    """
    Swap mutation - swaps two random positions.
    Modifies the board in-place.
    """
    a, b = random.sample(range(len(board)), 2)
    board[a], board[b] = board[b], board[a]

def print_board(board):
    """
    Print the chess board with queens for visualization.
    """
    n = len(board)
    print("\nBoard visualization:")
    print("  " + " ".join([str(i) for i in range(n)]))
    
    for row in range(n):
        line = f"{row} "
        for col in range(n):
            if board[col] == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()

def solve_nqueens_with_custom_params():
    """
    Solve N-Queens with custom parameters for demonstration.
    """
    print(f"=== Solving {N}-Queens Problem with Custom Parameters ===")
    
    # Create EA instance with custom parameters
    ea = EvolutionaryAlgorithm(
        population_size=100,
        max_generations=3000,
        mutation_rate=0.9,
        elitism_count=5,
        tournament_size=4
    )
    
    # Set problem-specific functions
    ea.set_problem_functions(
        fitness_func=fitness,
        crossover_func=crossover,
        mutation_func=mutate,
        init_func=random_board
    )
    
    # Calculate target fitness (perfect solution)
    max_pairs = N * (N - 1) // 2
    print(f"Target fitness (perfect solution): {max_pairs}")
    
    # Solve the problem
    solution, fitness_history = ea.evolve(target_fitness=max_pairs, verbose=True)
    
    # Display results
    final_fitness = fitness(solution)
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"{'='*50}")
    print(f"Best solution: {solution}")
    print(f"Final fitness: {final_fitness}")
    print(f"Perfect solution: {'Yes' if final_fitness == max_pairs else 'No'}")
    print(f"Success rate: {(final_fitness/max_pairs)*100:.2f}%")
    
    # Print the board
    print_board(solution)
    
    return solution, fitness_history

def solve_nqueens_original_params():
    """
    Solve N-Queens with original parameters from the old implementation.
    """
    print(f"=== Solving {N}-Queens Problem with Original Parameters ===")
    
    # Create EA instance with original parameters
    ea = EvolutionaryAlgorithm(
        population_size=80,
        max_generations=5000,
        mutation_rate=0.8,
        elitism_count=4,
        tournament_size=3
    )
    
    # Set problem-specific functions
    ea.set_problem_functions(
        fitness_func=fitness,
        crossover_func=crossover,
        mutation_func=mutate,
        init_func=random_board
    )
    
    # Calculate target fitness (perfect solution)
    max_pairs = N * (N - 1) // 2
    print(f"Target fitness (perfect solution): {max_pairs}")
    
    # Solve the problem
    solution, fitness_history = ea.evolve(target_fitness=max_pairs, verbose=True)
    
    # Display results
    final_fitness = fitness(solution)
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"{'='*50}")
    print(f"Best solution: {solution}")
    print(f"Final fitness: {final_fitness}")
    print(f"Perfect solution: {'Yes' if final_fitness == max_pairs else 'No'}")
    print(f"Success rate: {(final_fitness/max_pairs)*100:.2f}%")
    
    # Print the board
    print_board(solution)
    
    return solution, fitness_history

def compare_parameters():
    """
    Compare different parameter settings to demonstrate parameter tuning capability.
    """
    print("=== Parameter Comparison Demo ===")
    
    # Different parameter sets to compare
    param_sets = [
        {
            'name': 'Conservative',
            'params': {
                'population_size': 50,
                'max_generations': 2000,
                'mutation_rate': 0.3,
                'elitism_count': 2,
                'tournament_size': 3
            }
        },
        {
            'name': 'Aggressive',
            'params': {
                'population_size': 120,
                'max_generations': 1500,
                'mutation_rate': 0.9,
                'elitism_count': 8,
                'tournament_size': 5
            }
        },
        {
            'name': 'Balanced',
            'params': {
                'population_size': 80,
                'max_generations': 3000,
                'mutation_rate': 0.6,
                'elitism_count': 4,
                'tournament_size': 3
            }
        }
    ]
    
    max_pairs = N * (N - 1) // 2
    results = []
    
    for param_set in param_sets:
        print(f"\nTesting {param_set['name']} parameters...")
        print(f"Parameters: {param_set['params']}")
        
        ea = EvolutionaryAlgorithm(**param_set['params'])
        ea.set_problem_functions(
            fitness_func=fitness,
            crossover_func=crossover,
            mutation_func=mutate,
            init_func=random_board
        )
        
        solution, fitness_history = ea.evolve(target_fitness=max_pairs, verbose=False)
        final_fitness = fitness(solution)
        success_rate = (final_fitness/max_pairs)*100
        
        results.append({
            'name': param_set['name'],
            'fitness': final_fitness,
            'success_rate': success_rate,
            'generations': len(fitness_history)
        })
        
        print(f"Result: {final_fitness}/{max_pairs} ({success_rate:.2f}%) in {len(fitness_history)} generations")
    
    # Print comparison summary
    print(f"\n{'='*60}")
    print("PARAMETER COMPARISON SUMMARY:")
    print(f"{'='*60}")
    print(f"{'Parameter Set':<15} {'Fitness':<10} {'Success %':<12} {'Generations':<12}")
    print("-" * 60)
    
    for result in results:
        print(f"{result['name']:<15} {result['fitness']:<10} {result['success_rate']:<12.2f} {result['generations']:<12}")

def main():
    """
    Main function demonstrating the base evolutionary algorithm implementation.
    """
    print("Evolutionary Algorithm Base Implementation")
    print("=========================================")
    print(f"Problem: {N}-Queens")
    print(f"Goal: Place {N} queens on {N}x{N} board with no conflicts")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Solve with original parameters")
        print("2. Solve with custom parameters")
        print("3. Compare different parameter sets")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            solve_nqueens_original_params()
        elif choice == '2':
            solve_nqueens_with_custom_params()
        elif choice == '3':
            compare_parameters()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    # You can either run the interactive main() or directly call one function
    
    # For direct execution (uncomment one of these):
    # solve_nqueens_original_params()
    # solve_nqueens_with_custom_params()
    # compare_parameters()
    
    # For interactive menu:
    main()
