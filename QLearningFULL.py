from environment import EnvironmentConfig, Environment
import math
import time
import numpy as np
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


def run_epoch(env, qlearning, max_iterations):
    iteration = 0
    total_reward = 0
    env.reset()

    velocity, inclination, inclination_ahead, _, _ = env.step(0)
    start_state = [
        round(velocity),
        round(inclination),
        round(inclination_ahead)
    ]
    old_state = start_state
    qlearning.make_Q(old_state)

    while True:
        action = qlearning.make_move(old_state)

        velocity, inclination, inclination_ahead, reward, is_terminal = env.step(
            action)
        total_reward += reward

        new_state = [round(velocity), round(inclination),
                     round(inclination_ahead)]
        qlearning.make_Q(new_state)

        qlearning.default_learning(
            new_state, is_terminal, old_state, action, round(reward, 1))
        old_state = new_state

        iteration += 1
        if is_terminal:
            print(
                f"Reward: {total_reward:.1f},\tTarget reached in {iteration} iterations.")
            return True, iteration, total_reward
        if iteration > max_iterations:
            print(
                f"Reward: {total_reward:.1f},\tIteration limit. Target not reached")
            return False, iteration, total_reward


def run_test(env, qlearning, max_iterations):
    iteration = 0
    total_reward = 0
    env.reset()
    velocity, inclination, inclination_ahead, _, _ = env.step(0)
    state = [round(velocity), round(inclination),
             round(inclination_ahead)]

    while True:
        action = qlearning.make_move_optimal(state)

        velocity, inclination, inclination_ahead, reward, is_terminal = env.step(
            action)
        total_reward += reward

        state = [round(velocity), round(inclination),
                 round(inclination_ahead)]

        iteration += 1
        if is_terminal:
            print(
                f"Reward: {total_reward:.1f},\tTest success: {iteration} iterations.")
            return True, iteration, total_reward
        if iteration > max_iterations:
            print(f"Reward: {total_reward:.1f},\tIteration limit. Test failed")
            return False, iteration, total_reward


def learn(epochs, env, qlearning):
    start_time = time.time()
    iteration_counts = []
    rewards = []
    success_count = 0
    epoch_max_iterations = 5000

    for i in range(epochs):
        print(f"Epoch {i}:\t", end="")
        succeeded, iterations, reward = run_epoch(
            env, qlearning, epoch_max_iterations)
        iteration_counts.append(iterations)
        rewards.append(reward)
        if succeeded:
            success_count += 1

    print("Learning finished")
    print(f'Time: {round(time.time() - start_time, 2)}[s]')
    return success_count, iteration_counts, rewards


def test(epochs, env, qlearning):
    start_time = time.time()
    iteration_counts = []
    rewards = []
    success_count = 0
    epoch_max_iterations = 5000

    for i in range(epochs):
        print(f"Test {i}:\t", end="")
        succeeded, iterations, reward = run_test(
            env, qlearning, epoch_max_iterations)
        iteration_counts.append(iterations)
        rewards.append(reward)
        if succeeded:
            success_count += 1

    print("Learning finished")
    print(f'Time: {round(time.time() - start_time, 2)}[s]')
    return success_count, iteration_counts, rewards


points = [(0, 0), (3, 2), (6, -4), (9, 4), (12, -2), (15, 3),
          (18, -2), (21, 6), (24, 3), (27, 5), (30, -3)]

"""
2 metoda uczenia w QL

200k iter na uczenie
co 50k zmiana mapy

V > Vmax -> stan terminalny i zdycha -> dałbym 10

beta, gamma, epsilon, strategie wyboru akcji, modyfikacja nagród
poszukiwanie najlepszego agenta

dodać do danych średnią predkość
"""


config = EnvironmentConfig()
config.points = points
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

config.targetVelocity = 9.0
config.maxVelocity = 10.0

environment = Environment(config)

slope = environment.get_track_slope()
elevation = environment.get_track_elevation()

lines = []
lines.append(f'Gamma, Beta, Epsilon, Reached, Best, Worst, Average, Std\n')
if __name__ == "__main__":
    q = QLearningAlgorythm([-1, 0, 1], 0.9, 0.9, 0.2)
    l_reached, l_data, l_reward = learn(1000, environment, q)
    print(f'{25 * "#"}')
    t_reached, t_data, t_reward = test(1, environment, q)
    print(f'{25*"#"}')
    print("Learning data:")
    print(f"Reached targets:\t{l_reached}")
    print(f"Best time:\t{min(l_data)}")
    # print(f"Worst time: {max(l_data)}")
    print(f"Avg time: {np.average(l_data)}")
    # print(f"Std: {np.std(l_data)}")
    print(f"Best reward:\t{max(l_reward)}")
    print(f'{25 * "#"}')
    t_min = min(t_data)
    t_max = max(t_data)
    t_avg = np.average(t_data)
    t_std = np.std(t_data)
    print("Testing data:")
    print(f"Reached targets: {t_reached}")
    print(f"Best time: {t_min}")
    # print(f"Worst time: {t_max}")
    # print(f"Avg time: {t_avg}")
    # print(f"Std: {t_std}")
    print(f"Best reward:\t{max(t_reward)}")
    # lines.append(
    # f'{q.gamma}, {q.beta}, {q.epsilon}, {t_reached}, {t_min}, {t_max}, {t_avg}, {t_std}\n')
    # with open('out/QLdata.csv', 'w') as f:
    # for line in lines:
    # f.write(line)
