from environment import EnvironmentConfig, Environment
import math
import time
import numpy as np
import copy
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
LEARNING_TORS = [tor1, tor2, tor3, tor4, tor5]
tor6 = make_tor([1, 3, 8, -3, 4, 4, 5, -1, 8, -8])
tor7 = make_tor([-1, -3, 4, -1, 6, -1, -8, 7, -2, 0])
tor8 = make_tor([-2, 3, 3, 7, -1, -1, -8, -5, 0, -5])
TESTING_TORS = [tor6, tor7, tor8]


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
            return True, iteration, total_reward, qlearning
        if iteration > max_iterations:
            print(
                f"Reward: {total_reward:.1f},\tIteration limit. Target not reached")
            return False, iteration, total_reward, qlearning


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


def learn(epochs, config, qlearning):
    start_time = time.time()
    iteration_counts = []
    rewards = []
    success_count = 0
    epoch_max_iterations = 5000

    for i in range(epochs):
        config.points = LEARNING_TORS[int(math.floor(i/100))]
        env = Environment(config)

        print(f"Epoch {i}:\t", end="")
        succeeded, iterations, reward, qlearning = run_epoch(
            env, qlearning, epoch_max_iterations)
        iteration_counts.append(iterations)
        rewards.append(reward)
        if succeeded:
            success_count += 1

    print("Learning finished")
    print(f'Time: {round(time.time() - start_time, 2)}[s]')
    return success_count, iteration_counts, rewards, qlearning


def test(epochs, config, qlearning):
    start_time = time.time()
    iteration_counts = []
    rewards = []
    success_count = 0
    epoch_max_iterations = 5000

    for i in range(epochs):
        config.points = LEARNING_TORS[int(math.floor(i / 3))]
        env = Environment(config)

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


"""
2 metoda uczenia w QL

200k iter na uczenie
co 50k zmiana mapy

V > Vmax -> stan terminalny i zdycha -> dałbym 10

beta, gamma, epsilon, strategie wyboru akcji, modyfikacja nagród
poszukiwanie najlepszego agenta

dodać do danych średnią predkość
"""


# test 1 szukanie najlepszych gamma, beta i epsilon
lines = []
lines.append(f'Gamma, Beta, Epsilon, Reached, Best, Worst, Average, Std, BestReward\n')
if __name__ == "__main__":

    config = EnvironmentConfig()
    # config.points = tor1
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

    betas = [0.1, 0.5, 0.9]  # 0.1, 0.5, 0.9
    gammas = [0.1, 0.5, 0.9]  # 0.1, 0.5, 0.9
    epsys = [0, 5, 10, 20, 25]  # 0, 5, 10, 20, 25
    for eps in epsys:
        for beta in betas:
            for gamma in gammas:
                print(f'{40*"#"}')
                print(f'Testing params: beta: {beta}, gamma: {gamma}, epsilon: {eps}')
                q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=eps)
                l_reached, l_data, l_reward, q = learn(500, config, q)
                print(f'{25 * "#"}')
                t_reached, t_data, t_reward = test(9, config, q)
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
                print(f"Avg time: {t_avg}")
                # print(f"Std: {t_std}")
                print(f"Best reward:\t{max(t_reward)}")

                lines.append(
                f'{q.gamma}, {q.beta}, {q.epsilon}, {t_reached}, {t_min}, {t_max}, {t_avg}, {t_std}, {max(t_reward)}\n')
    with open('out/QLdata.csv', 'w') as f:
        for line in lines:
            f.write(line)
