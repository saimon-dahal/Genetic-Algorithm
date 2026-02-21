import sys

import pygame

from config.config import settings
from src.grid import Grid


def main() -> None:
    pygame.init()

    WIDTH: int = settings.display.width
    HEIGHT: int = settings.display.height
    GRID_SIZE: int = settings.simulation.grid_size
    NUM_CREATURES: int = settings.simulation.num_creatures
    CELL_SIZE: int = WIDTH // GRID_SIZE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Creature Evolution Simulation")

    generation_duration = 300  # frames per generation
    grid = Grid(
        GRID_SIZE, GRID_SIZE, NUM_CREATURES, steps_per_generation=generation_duration
    )

    font = pygame.font.Font(None, 36)
    WHITE = tuple(settings.colors.white)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid.update()

        screen.fill(WHITE)
        grid.draw(screen, CELL_SIZE)

        generation_text = font.render(f"Generation: {grid.generation}", True, (0, 0, 0))
        screen.blit(generation_text, (10, 10))

        if grid.generation > 0:
            survival_text = font.render(
                f"Previous Gen Survival:{grid.survival_rate:.2f}%", True, (0, 0, 0)
            )
            screen.blit(survival_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
