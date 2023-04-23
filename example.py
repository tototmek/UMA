from environment import EnvironmentConfig, Environment
import math
import pygame
import time

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

config = EnvironmentConfig()
config.points = points
config.trackLength = 24
config.cartThrustGain = 16.0
config.gravity = 9.81
config.efficiency = 0.995
config.simDeltatime = 0.005
config.simStepsPerStep = 6
config.inclinationLookAheadDistance = 1.0
config.positionRewardGain = 1.0
config.velocityRewardGain = 0.0
config.timePenaltyGain = 0.1
config.reversingPenaltyGain = 0.0
config.overspeedPenaltyGain = 0.0
config.finishRewardGain = 42.0
config.targetVelocity = 1.0
config.maxVelocity = 10.0

environment = Environment(config)

slope = environment.get_track_slope()
elevation = environment.get_track_elevation()

pygame.init()
window = pygame.display.set_mode((960, 540))
pygame.display.set_caption("RViz")
scale = 30
offset_x = 50
offset_y = 300

(black, grey, darkgrey, white) = ((0, 0, 0),
                                  (48, 48, 48), (20, 20, 20), (255, 255, 255))

deltatime = 0.017


def draw_circle_at(x, y, color=white):
    pygame.draw.circle(window, color, (x, y), 5)


def draw_circle(position, elevation_map, color=white):
    draw_circle_at(position * scale + offset_x, offset_y -
                   elevation_map(position) * scale, color)


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

i = 1
running = True
environment.reset()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    thrust = 0.0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        thrust = 1.0
    if keys[pygame.K_LEFT]:
        thrust = -1.0
    if keys[pygame.K_r]:
        environment.reset()

    velocity, inclination, inclination_ahead, reward, is_terminal = environment.step(
        thrust)
    cart_x = environment.get_cart_position()
    print(f"Position: {cart_x:>6.2f}\tVelocity: {velocity:>6.2f}\tInclination: {inclination:>6.2f}\tInc.Ahead: {inclination_ahead:>6.2f}\tReward: {reward:>6.2f}\tisTerminal: {is_terminal}")
    i += 1
    if is_terminal:
        print(i)
        running = False
    window.fill(black)
    draw_axes()
    draw_track(slope, 31, darkgrey)
    lookahead_position = cart_x + config.inclinationLookAheadDistance
    draw_circle(lookahead_position, elevation, grey)
    draw_track(elevation, 31)
    draw_circle(cart_x, elevation)
    pygame.display.update()
    time.sleep(deltatime)

pygame.quit()
