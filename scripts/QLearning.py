from environment import EnvironmentConfig, Environment
import math
import pygame
import time
from scripts.QL import QLearningAlgorythm


"""
Założenia:
Algorytm ma 100k iteracji na naukę
potem ma 10K iteracji testujących
Kryterium porównawcze:
Liczność osiągnieć celu podczas testów
Ograniczenia:
maksymalna prędkość 10 - powyżej 10 stan terminalny
Dodatkowe elementy algorytmu uczącego:

"""

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

config.targetVelocity = 9.0
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


running = True
environment.reset()
q = QLearningAlgorythm([-1, 0, 1], 0.9, 0.9, 0.25)
iter = 1
reached = 0
last_reached = 0

thrust = 0.0
velocity, inclination, inclination_ahead, reward, is_terminal = environment.step(0)
start_state = [round(velocity), round(inclination), round(inclination_ahead)]
old_state = start_state
q.make_Q(old_state)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = q.make_move(old_state)
    if action == 1:
        thrust = 1.0
    elif action == 0:
        thrust = 0.0
    else:
        thrust = -1.0

    velocity, inclination, inclination_ahead, reward, is_terminal = environment.step(thrust)
    new_state = [round(velocity), round(inclination), round(inclination_ahead)]
    q.make_Q(new_state)

    q.default_learning(new_state, is_terminal, old_state, action, round(reward, 1))
    old_state = new_state

    if is_terminal:
        reached += 1
        print(f"Target reached in {iter-last_reached} iterations")
        # q.save_Q(f"QLKnowledge/reach{reached}_iter{iter}")
        last_reached = iter
        environment.reset()
        old_state = start_state
        if reached >= 50:
            running = False

    iter += 1

    cart_x = environment.get_cart_position()

    window.fill(black)
    draw_axes()
    draw_track(slope, 31, darkgrey)
    lookahead_position = cart_x + config.inclinationLookAheadDistance
    draw_circle(lookahead_position, elevation, grey)
    draw_track(elevation, 31)
    draw_circle(cart_x, elevation)
    pygame.display.update()
    #time.sleep(deltatime)

pygame.quit()
