from environment import EnvironmentConfig, Environment
import math
import pygame
import time
from scripts.QL import QLearningAlgorythm


def make_tor(Ys):
    tor = [(0, 0)]
    x = 3
    for y in Ys:
        tor.append((x, y))
        x += 3
    return tor


tor1 = make_tor([2, -4, 4, -2, 3, -2, 6, 3, 5, -3])
tor2 = make_tor([-3, 5, 3, 6, -2, 3, -2, 4, -4, 2])
tor3 = make_tor([0, 6, -4, -8, -6, 4, -1, -2, 3, 2])
tor4 = make_tor([-7, 4, 6, 6, -2, 6, 6, 4, 2, 3])
tor5 = make_tor([2, 2, -4, -7, 8, -7, -6, -6, -4, -3])
LEARNING_TRACKS = [tor1, tor2, tor3, tor4, tor5]
tor6 = make_tor([1, 3, 8, -3, 4, 4, 5, -1, 8, -8])
tor7 = make_tor([-1, -3, 4, -1, 6, -1, -8, 7, -2, 0])
tor8 = make_tor([-2, 3, 3, 7, -1, -1, -8, -5, 0, -5])
TESTING_TRACKS = [tor6, tor7, tor8]
tor10 = make_tor([-8, 8, -7, 7, -8, 8, -6, 6, 5, 5])

targetV = 9.0
config = EnvironmentConfig()
config.points = tor10  # tor do wyboru
config.trackLength = 30
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
config.targetVelocity = targetV
config.maxVelocity = 10.0

environment = Environment(config)

slope = environment.get_track_slope()
elevation = environment.get_track_elevation()

pygame.init()

font = pygame.font.Font(None, 36)

window = pygame.display.set_mode((960, 540))
pygame.display.set_caption("RViz")
scale = 30
offset_x = 50
offset_y = 300

(black, grey, darkgrey, white, red) = ((0, 0, 0),
                                  (48, 48, 48), (20, 20, 20), (255, 255, 255), (255, 0, 0))

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
agent = QLearningAlgorythm([-1, 0, 1], gamma=0.9, beta=0.1, epsilon=0, t=0.25)
agent.load_Q("../QLKnowledge/bestAgent.json")
velocity, inclination, inclination_ahead, _, _ = environment.step(0)
state = [str(round(velocity)), str(round(inclination)), str(round(inclination_ahead))]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = agent.make_move_optimal(state)

    velocity, inclination, inclination_ahead, reward, is_terminal = environment.step(int(action))

    state = [str(round(velocity)), str(round(inclination)),
             str(round(inclination_ahead))]

    cart_x = environment.get_cart_position()
    print(f"Position: {cart_x:>6.2f}\tVelocity: {velocity:>6.2f}\tInclination: {inclination:>6.2f}\tInc.Ahead: {inclination_ahead:>6.2f}\tReward: {reward:>6.2f}\tisTerminal: {is_terminal}")
    i += 1
    if is_terminal:
        print(f"Target achieved in: {i} iterations.")
        running = False
    window.fill(black)
    draw_axes()
    draw_track(slope, 31, darkgrey)
    lookahead_position = cart_x + config.inclinationLookAheadDistance
    draw_circle(lookahead_position, elevation, grey)
    draw_track(elevation, 31)
    draw_circle(cart_x, elevation)
    v_obecna_text = font.render("V obecna: " + str(f'{velocity:>6.2f}'), True, red if velocity > targetV else white)
    v_zadana_text = font.render("V zadana: " + str(targetV), True, white)
    window.blit(v_obecna_text, (10, 10))
    window.blit(v_zadana_text, (10, 50))
    pygame.display.update()
    time.sleep(deltatime)

pygame.quit()
