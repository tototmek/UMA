import engine
import pygame
import time
from scripts.track import Track


points = [
    (0, 3),
    (5, -1),
    (10, 5),
    (15, 4),
    (20, 3),
]
track = Track.through_points(points)


simulation = engine.Simulation(track.coeffs)

pygame.init()
window = pygame.display.set_mode((960, 540))
scale = 30
offset_x = 50
offset_y = 300

(black, grey, darkgrey, white) = ((0, 0, 0),
                                  (48, 48, 48), (20, 20, 20), (255, 255, 255))

deltatime = 0.017
sim_resolution = 5


def draw_circle(x, y):
    pygame.draw.circle(window, white, (x, y), 5)


def draw_track(track_elevation, length, color=white):
    step = 0.1
    x = 0
    while x < length:
        pygame.draw.line(window, color, (x * scale + offset_x, offset_y - track_elevation(x) * scale),
                         ((x + step) * scale + offset_x, offset_y - track_elevation(x + step) * scale))
        x += step


def draw_axes(color=darkgrey):
    pygame.draw.line(window, color, (0, offset_y), (960, offset_y))
    pygame.draw.line(window, color, (offset_x, 0), (offset_x, 540))


# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    thrust = 0.0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        thrust = 16.0
    if keys[pygame.K_LEFT]:
        thrust = -16.0

    window.fill(black)
    simulation.step_multiple(
        deltatime=deltatime/sim_resolution,
        cartThrust=thrust,
        steps=sim_resolution)
    cart_x = simulation.getCartPosition()
    draw_axes()
    draw_track(track.slope, 100, grey)
    draw_track(track.elevation, 100)
    draw_circle(cart_x * scale + offset_x, offset_y -
                track.elevation(cart_x) * scale)
    pygame.display.update()
    time.sleep(deltatime)

# Quit pygame
pygame.quit()
