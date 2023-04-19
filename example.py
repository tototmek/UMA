import engine
import pygame
import time


def track_elevation(x): return - 3 * x + 0.07 * x**2


def track_inclination(x): return -3 + 0.14 * x


simulation = engine.Simulation(track_inclination=track_inclination)

pygame.init()
window = pygame.display.set_mode((960, 540))
scale = 10
offset_x = 100
offset_y = 200

(black, white) = ((0, 0, 0), (255, 255, 255))


def draw_circle(x, y):
    pygame.draw.circle(window, white, (x, y), 5)


def draw_track(track_elevation, length):
    step = 0.1
    x = 0
    while x < length:
        pygame.draw.line(window, white, (x * scale + offset_x, offset_y - track_elevation(x) * scale),
                         ((x + step) * scale + offset_x, offset_y - track_elevation(x + step) * scale))
        x += step


# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(black)
    simulation.step(0.1, 0.0)
    cart_x = simulation.getCartPosition()
    draw_circle(cart_x * scale + offset_x, offset_y -
                track_elevation(cart_x) * scale)
    draw_track(track_elevation, 20)
    pygame.display.update()
    time.sleep(0.017)

# Quit pygame
pygame.quit()
