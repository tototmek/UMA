import engine
import math
import pygame
import time
from scripts.track_generation import TrackGenerator


points = [
    (0, 0),
    (3, 2),
    (6, -4),
    (9, 4),
    (12, -2),
    (15, 3),
    (18, -2),
    (21, 6),
    (24, 3),
    (27, 5),
    (30, -3),

]


simulation = engine.Simulation(points)
slope = simulation.get_track_slope()
elevation = simulation.get_track_elevation()

pygame.init()
window = pygame.display.set_mode((960, 540))
pygame.display.set_caption("RViz")
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
    step = 0.2
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
        thrust = 32.0
    if keys[pygame.K_LEFT]:
        thrust = -32.0
    if keys[pygame.K_r]:
        simulation.reset()

    window.fill(black)
    simulation.step_multiple(
        deltatime=deltatime/sim_resolution,
        cartThrust=thrust,
        steps=sim_resolution)
    cart_x = simulation.get_cart_position()
    draw_axes()
    draw_track(slope, 31, darkgrey)
    draw_track(elevation, 31)
    draw_circle(cart_x * scale + offset_x, offset_y -
                elevation(cart_x) * scale)
    pygame.display.update()
    time.sleep(deltatime)

# Quit pygame
pygame.quit()
