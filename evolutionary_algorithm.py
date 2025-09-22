import random
from typing import List, Callable, Tuple, Any

class EvolutionaryAlgorithm:
    """Base implementation of an Evolutionary Algorithm that can be used for parameter tuning."""
    
    def __init__(self, 
                 population_size: int = 100,
                 max_generations: int = 1000,
                 mutation_rate: float = 0.1,
                 elitism_count: int = 2,
                 tournament_size: int = 3):
        """
        Initialize the Evolutionary Algorithm with configurable parameters.
        
        Args:
            population_size: Size of the population
            max_generations: Maximum number of generations
            mutation_rate: Probability of mutation
            elitism_count: Number of elite individuals to preserve
            tournament_size: Size of tournament for selection
        """
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        self.tournament_size = tournament_size
        
        # These will be set by the problem-specific implementation
        self.fitness_function: Callable = None
        self.crossover_function: Callable = None
        self.mutation_function: Callable = None
        self.initialization_function: Callable = None
        
    def set_problem_functions(self,
                            fitness_func: Callable,
                            crossover_func: Callable,
                            mutation_func: Callable,
                            init_func: Callable):
        """Set the problem-specific functions."""
        self.fitness_function = fitness_func
        self.crossover_function = crossover_func
        self.mutation_function = mutation_func
        self.initialization_function = init_func
    
    def initialize_population(self) -> List[Any]:
        """Initialize the population using the provided initialization function."""
        if not self.initialization_function:
            raise ValueError("Initialization function not set")
        return [self.initialization_function() for _ in range(self.population_size)]
    
    def evaluate_population(self, population: List[Any]) -> List[float]:
        """Evaluate fitness for entire population."""
        if not self.fitness_function:
            raise ValueError("Fitness function not set")
        return [self.fitness_function(individual) for individual in population]
    
    def tournament_selection(self, population: List[Any]) -> Any:
        """Tournament selection."""
        contestants = random.sample(population, min(self.tournament_size, len(population)))
        return max(contestants, key=self.fitness_function)
    
    def create_offspring(self, population: List[Any]) -> List[Any]:
        """Create offspring through crossover and mutation."""
        offspring = []
        
        # Keep elite individuals
        sorted_pop = sorted(population, key=self.fitness_function, reverse=True)
        offspring.extend(sorted_pop[:self.elitism_count])
        
        # Generate remaining offspring
        while len(offspring) < self.population_size:
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            
            child = self.crossover_function(parent1, parent2)
            
            if random.random() < self.mutation_rate:
                self.mutation_function(child)
            
            offspring.append(child)
        
        return offspring
    
    def evolve(self, target_fitness: float = None, verbose: bool = True) -> Tuple[Any, List[float]]:
        """
        Main evolution loop.
        
        Args:
            target_fitness: Stop when this fitness is reached (optional)
            verbose: Print progress information
            
        Returns:
            Tuple of (best_individual, fitness_history)
        """
        if not all([self.fitness_function, self.crossover_function, 
                   self.mutation_function, self.initialization_function]):
            raise ValueError("All problem functions must be set before evolution")
        
        population = self.initialize_population()
        fitness_history = []
        
        for generation in range(self.max_generations):
            # Evaluate population
            fitness_scores = self.evaluate_population(population)
            best_fitness = max(fitness_scores)
            avg_fitness = sum(fitness_scores) / len(fitness_scores)
            
            fitness_history.append(best_fitness)
            
            if verbose:
                print(f"Generation {generation}: Best = {best_fitness:.4f}, Avg = {avg_fitness:.4f}")
            
            # Check termination condition
            if target_fitness and best_fitness >= target_fitness:
                if verbose:
                    print(f"✅ Target fitness {target_fitness} reached in generation {generation}")
                break
            
            # Create next generation
            population = self.create_offspring(population)
        
        # Return best individual
        final_fitness = self.evaluate_population(population)
        best_idx = final_fitness.index(max(final_fitness))
        best_individual = population[best_idx]
        
        return best_individual, fitness_history
    
    def get_parameters(self) -> dict:
        """Get current algorithm parameters for tuning."""
        return {
            'population_size': self.population_size,
            'max_generations': self.max_generations,
            'mutation_rate': self.mutation_rate,
            'elitism_count': self.elitism_count,
            'tournament_size': self.tournament_size
        }
    
    def set_parameters(self, **kwargs):
        """Set algorithm parameters for tuning."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown parameter: {key}")
