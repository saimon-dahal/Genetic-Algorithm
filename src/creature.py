import random

from src.neural_network import NeuralNetwork


class Creature:
    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.genome = self.generate_genome()
        self.brain = NeuralNetwork(self.genome)
        self.color = self.genome_to_color()
        self.age = 0
        self.fitness = 0
        self.last_move_x = 0
        self.last_move_y = 0

    def generate_genome(self):
        # Calculate required genome length
        input_size = 7
        hidden_size = 4
        output_size = 8
        required_weights = (input_size * hidden_size) + (hidden_size * output_size)
        genome_length = required_weights * 2  # 2 hex chars per weight
        return "".join(
            format(random.randint(0, 255), "02x") for _ in range(genome_length // 2)
        )

    def genome_to_color(self):
        return tuple(int(self.genome[i : i + 2], 16) for i in (0, 2, 4))

    def get_inputs(self, grid):
        return [
            self.x / self.grid_size,
            self.y / self.grid_size,
            grid.get_population_density(self.x, self.y, radius=2),
            self.age / 100,  # Normalize age
            random.random(),
            self.last_move_x / self.grid_size,
            self.last_move_y / self.grid_size,
        ]

    def move(self, grid):
        inputs = self.get_inputs(grid)
        outputs = self.brain.activate(inputs)
        self.perform_actions(outputs, grid)
        self.age += 1

    def perform_actions(self, outputs, grid):
        dx = round(outputs[0] - outputs[1])
        dy = round(outputs[2] - outputs[3])
        new_x = max(0, min(self.grid_size - 1, self.x + dx))
        new_y = max(0, min(self.grid_size - 1, self.y + dy))

        if grid.grid[new_y][new_x] is None:
            grid.grid[self.y][self.x] = None
            self.last_move_x = new_x - self.x
            self.last_move_y = new_y - self.y
            self.x, self.y = new_x, new_y
            grid.grid[self.y][self.x] = self

        # Use the fifth output for "eating" (gaining fitness)
        self.fitness += max(0, outputs[4])

    def calculate_fitness(self):
        center_x, center_y = self.grid_size / 2, self.grid_size / 2
        distance_from_center = (
            (self.x - center_x) ** 2 + (self.y - center_y) ** 2
        ) ** 0.5
        position_fitness = 1 - (distance_from_center / (self.grid_size / 2))
        self.fitness = self.fitness * 0.7 + position_fitness * 0.3

    @staticmethod
    def crossover(parent1, parent2):
        crossover_point = (
            random.randint(1, 7) * 4
        )  # Ensure crossover at gene boundaries
        child_genome = (
            parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
        )
        return child_genome

    @staticmethod
    def mutate(genome, mutation_rate=0.01):
        return "".join(
            format(
                (
                    int(g, 16) ^ (1 << random.randint(0, 3))
                    if random.random() < mutation_rate
                    else int(g, 16)
                ),
                "02x",
            )
            for g in [genome[i : i + 2] for i in range(0, len(genome), 2)]
        )

    @classmethod
    def create_offspring(cls, parent1, parent2, grid_size):
        child_genome = cls.mutate(cls.crossover(parent1, parent2))
        child = cls(
            random.randint(0, grid_size - 1),
            random.randint(0, grid_size - 1),
            grid_size,
        )
        child.genome = child_genome
        child.brain = NeuralNetwork(child_genome)
        child.color = child.genome_to_color()
        return child
