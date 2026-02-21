import random

import pygame

from src.creature import Creature


class Grid:
    def __init__(self, width, height, num_creatures, steps_per_generation):
        self.width = width
        self.height = height
        self.generation = 0
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.creatures = []
        self.populate(num_creatures)
        self.survival_rate = 0
        self.steps_per_generation = steps_per_generation
        self.current_step = 0

    def populate(self, num_creatures):
        for _ in range(num_creatures):
            while True:
                x, y = (
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1),
                )
                if self.grid[y][x] is None:
                    creature = Creature(x, y, self.width)
                    self.grid[y][x] = creature
                    self.creatures.append(creature)
                    break

    def update(self):
        random.shuffle(self.creatures)
        for creature in self.creatures:
            creature.move(self)

        self.current_step += 1
        if self.current_step >= self.steps_per_generation:
            self.evolve()
            self.current_step = 0

    def evolve(self):
        surviving_creatures = [
            creature for creature in self.creatures if creature.x >= self.width // 2
        ]

        # calculate survival rate
        self.survival_rate = len(surviving_creatures) / len(self.creatures) * 100
        if not surviving_creatures:
            new_population = [
                Creature(
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1),
                    self.width,
                )
                for _ in range(len(self.creatures))
            ]
        else:
            new_population = []
            while len(new_population) < len(self.creatures):
                parent1, parent2 = random.sample(surviving_creatures, 2)
                child = Creature.create_offspring(parent1, parent2, self.width)
                new_population.append(child)

        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        for creature in new_population:
            while True:
                x, y = (
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1),
                )
                if self.grid[y][x] is None:
                    creature.x, creature.y = x, y
                    self.grid[y][x] = creature
                    break

        self.creatures = new_population
        self.generation += 1

    def draw(self, screen, cell_size):
        for creature in self.creatures:
            pygame.draw.rect(
                screen,
                creature.color,
                (creature.x * cell_size, creature.y * cell_size, cell_size, cell_size),
            )

    def get_population_density(self, x, y, radius=1):
        """Calculate population density around a given point."""
        count = 0
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] is not None:
                        count += 1
        return count / ((2 * radius + 1) ** 2)
