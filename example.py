import engine
import pygame
import time


simulation = engine.Simulation(track_inclination=lambda x: 0.1 * x)

pygame.init()
window = pygame.display.set_mode((960, 540))

(black, white) = ((0, 0, 0), (255, 255, 255))


def draw_circle(x, y):
    pygame.draw.circle(window, white, (x, y), 5)


# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(black)
    simulation.step(0.1, 0.0)
    draw_circle(simulation.getCartPosition(), 200)
    pygame.display.update()
    time.sleep(0.017)

# Quit pygame
pygame.quit()
