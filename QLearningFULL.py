import random

from environment import EnvironmentConfig, Environment
import math
import time
import numpy as np
import copy
from collections import Counter
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


def run_epoch(env, qlearning, max_iterations, is_Boltzamann):
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
        if not is_Boltzamann:
            action = qlearning.make_move_greedy(old_state)
        else:
            action = qlearning.make_move_Boltzmann(state=old_state)

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


def run_test(env, qlearning, max_iterations, hive=False):
    iteration = 0
    total_reward = 0
    env.reset()
    velocity, inclination, inclination_ahead, _, _ = env.step(0)
    state = [round(velocity), round(inclination),
             round(inclination_ahead)]

    while True:
        if hive is False:
            action = qlearning.make_move_optimal(state)
        else:
            actions = [q.make_move_optimal(state) for q in qlearning]
            counter = Counter(actions)
            max_count = max(counter.values())
            most_common_values = [num for num, count in counter.items() if count == max_count]
            if len(most_common_values) > 1:
                action = random.choice(most_common_values)
            else:
                action = most_common_values[0]

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


def learn(epochs, config, qlearning, is_Boltzamann=False, track=None):
    start_time = time.time()
    iteration_counts = []
    rewards = []
    success_count = 0
    epoch_max_iterations = 5000

    for i in range(epochs):
        if track is None:
            config.points = LEARNING_TRACKS[int(math.floor(i/(epochs/5)))]
            env = Environment(config)
        else:
            config.points = LEARNING_TRACKS[track]
            env = Environment(config)

        print(f"Epoch {i}:\t", end="")
        succeeded, iterations, reward, qlearning = run_epoch(
            env, qlearning, epoch_max_iterations, is_Boltzamann)
        iteration_counts.append(iterations)
        rewards.append(reward)
        if succeeded:
            success_count += 1

    print("Learning finished")
    print(f'Time: {round(time.time() - start_time, 2)}[s]')
    return success_count, iteration_counts, rewards, qlearning


def test(epochs, config, qlearning, hive=False):
    start_time = time.time()

    iteration_counts = []
    rewards = []
    success_count = 0
    epoch_max_iterations = 5000

    for i in range(epochs):
        config.points = TESTING_TRACKS[int(math.floor(i / 3))]
        env = Environment(config)

        print(f"Test {i}:\t", end="")
        succeeded, iterations, reward = run_test(
            env, qlearning, epoch_max_iterations, hive)
        iteration_counts.append(iterations)
        rewards.append(reward)
        if succeeded:
            success_count += 1

    print("testing finished")
    print(f'Time: {round(time.time() - start_time, 2)}[s]')
    return success_count, iteration_counts, rewards


def test_params_E(config):  # epsilon zachłanna
    lines = []
    lines.append(f'Gamma, Beta, Epsilon, LearningReached, TestingReached, Best, Worst, Average, Std, BestReward\n')

    gammas = [0.1, 0.5, 0.9]  # 0.1, 0.5, 0.9
    betas = [0.1, 0.5, 0.9]  # 0.1, 0.5, 0.9
    epsys = [0, 5, 10, 20, 25]  # 0, 5, 10, 20, 25
    it = 250
    t = 0
    for eps in epsys:
        for beta in betas:
            for gamma in gammas:
                avg_l_reached, avg_t_reached, avg_t_min, avg_t_max, avg_t_avg, avg_t_std, avg_t_reward = [], [], [], [], [], [], []

                for repeat in range(10):
                    print(f'{40 * "#"}')
                    print(f'Testing params: beta: {beta}, gamma: {gamma}, epsilon: {eps}, t: {t}, iter: {it}')
                    q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=eps, t=t)
                    l_reached, l_data, l_reward, q = learn(it, config, q, is_Boltzamann=False)  # it=500
                    print(f'{25 * "#"}')
                    t_reached, t_data, t_reward = test(9, config, q)
                    print(f'{25 * "#"}')
                    print("Learning data:")
                    print(f"Reached targets:\t{l_reached}")
                    print(f"Best time:\t{min(l_data)}")
                    print(f"Avg time: {np.average(l_data)}")
                    print(f"Best reward:\t{max(l_reward)}")
                    print(f'{25 * "#"}')
                    t_min = min(t_data)
                    t_max = max(t_data)
                    t_avg = np.average(t_data)
                    t_std = np.std(t_data)
                    print("Testing data:")
                    print(f"Reached targets: {t_reached}")
                    print(f"Best time: {t_min}")
                    print(f"Avg time: {t_avg}")
                    print(f"Best reward:\t{max(t_reward)}")
                    avg_l_reached.append(l_reached)
                    avg_t_reached.append(t_reached)
                    avg_t_min.append(t_min)
                    avg_t_max.append(t_max)
                    avg_t_avg.append(t_avg)
                    avg_t_std.append(t_avg)
                    avg_t_reward.append(max(t_reward))

                lines.append(
                f'{gamma}, {beta}, {eps}, {np.average(avg_l_reached)}, {np.average(avg_t_reached)}, '
                f'{np.average(avg_t_min)}, {np.average(avg_t_max)}, {np.average(avg_t_avg)}, {np.average(avg_t_std)}, '
                f'{np.average(avg_t_reward)}\n')
    with open('out/QLdata_fulldata_epsilon.csv', 'w') as f:
        for line in lines:
            f.write(line)


def test_params_T(config):  # strategia boltzmanna
    lines = []
    lines.append(f'Gamma, Beta, T, LearningReached, TestingReached, Best, Worst, Average, Std, BestReward\n')

    gammas = [0.1, 0.5, 0.9]  # 0.1, 0.5, 0.9
    betas = [0.1, 0.5, 0.9]  # 0.1, 0.5, 0.9
    t = [0.25, 0.5, 0.75, 1]
    eps = 0
    it = 250
    for t in t:
        for beta in betas:
            for gamma in gammas:
                avg_l_reached, avg_t_reached, avg_t_min, avg_t_max, avg_t_avg, avg_t_std, avg_t_reward = [], [], [], [], [], [], []

                for repeat in range(10):
                    print(f'{40 * "#"}')
                    print(f'Testing params: beta: {beta}, gamma: {gamma}, epsilon: {eps}, t: {t}, iter: {it}')
                    q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=eps, t=t)
                    l_reached, l_data, l_reward, q = learn(it, config, q, is_Boltzamann=True)  # it=500
                    print(f'{25 * "#"}')
                    t_reached, t_data, t_reward = test(9, config, q)
                    print(f'{25 * "#"}')
                    print("Learning data:")
                    print(f"Reached targets:\t{l_reached}")
                    print(f"Best time:\t{min(l_data)}")
                    print(f"Avg time: {np.average(l_data)}")
                    print(f"Best reward:\t{max(l_reward)}")
                    print(f'{25 * "#"}')
                    t_min = min(t_data)
                    t_max = max(t_data)
                    t_avg = np.average(t_data)
                    t_std = np.std(t_data)
                    print("Testing data:")
                    print(f"Reached targets: {t_reached}")
                    print(f"Best time: {t_min}")
                    print(f"Avg time: {t_avg}")
                    print(f"Best reward:\t{max(t_reward)}")
                    avg_l_reached.append(l_reached)
                    avg_t_reached.append(t_reached)
                    avg_t_min.append(t_min)
                    avg_t_max.append(t_max)
                    avg_t_avg.append(t_avg)
                    avg_t_std.append(t_avg)
                    avg_t_reward.append(max(t_reward))

                lines.append(
                f'{gamma}, {beta}, {t}, {np.average(avg_l_reached)}, {np.average(avg_t_reached)}, '
                f'{np.average(avg_t_min)}, {np.average(avg_t_max)}, {np.average(avg_t_avg)}, {np.average(avg_t_std)}, '
                f'{np.average(avg_t_reward)}\n')
    with open('out/QLdata_fulldata_T.csv', 'w') as f:
        for line in lines:
            f.write(line)


def test_saturation(config):
    lines = []
    lines.append(f'Iters, LearningReached, TestingReached, Best, Worst, Average, Std, BestReward\n')

    gamma = 0.9
    beta = 0.1
    t = 0.25
    iters = [5, 10, 25, 50, 75, 100, 150, 200, 250, 500, 1000]
    for it in iters:
        avg_l_reached, avg_t_reached, avg_t_min, avg_t_max, avg_t_avg, avg_t_std, avg_t_reward = [], [], [], [], [], [], []

        for repeat in range(10):
            print(f'{40 * "#"}')
            print(f'Testing params: beta: {beta}, gamma: {gamma}, t: {t}, iter: {it}')
            q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=0, t=t)
            l_reached, l_data, l_reward, q = learn(it, config, q, is_Boltzamann=True)
            print(f'{25 * "#"}')
            t_reached, t_data, t_reward = test(9, config, q)
            print(f'{25 * "#"}')
            print("Learning data:")
            print(f"Reached targets:\t{l_reached}")
            print(f"Best time:\t{min(l_data)}")
            print(f"Avg time: {np.average(l_data)}")
            print(f"Best reward:\t{max(l_reward)}")
            print(f'{25 * "#"}')
            t_min = min(t_data)
            t_max = max(t_data)
            t_avg = np.average(t_data)
            t_std = np.std(t_data)
            print("Testing data:")
            print(f"Reached targets: {t_reached}")
            print(f"Best time: {t_min}")
            print(f"Avg time: {t_avg}")
            print(f"Best reward:\t{max(t_reward)}")
            avg_l_reached.append(l_reached)
            avg_t_reached.append(t_reached)
            avg_t_min.append(t_min)
            avg_t_max.append(t_max)
            avg_t_avg.append(t_avg)
            avg_t_std.append(t_avg)
            avg_t_reward.append(max(t_reward))

        lines.append(
            f'{it}, {np.average(avg_l_reached)}, {np.average(avg_t_reached)}, '
            f'{np.average(avg_t_min)}, {np.average(avg_t_max)}, {np.average(avg_t_avg)}, {np.average(avg_t_std)}, '
            f'{np.average(avg_t_reward)}\n')
    with open('out/QLdata_fulldata_saturation_150.csv', 'w') as f:
        for line in lines:
            f.write(line)


def test_hive5_vs1(config):
    lines = []
    lines.append(f'SoloLearningReached, SoloTestingReached, SoloBest, SoloWorst, SoloAverage, SoloStd, SoloAverageReward,'
                 f' HiveLearningReached, HiveTestingReached, HiveBest, HiveWorst, HiveAverage, HiveStd, HiveAverageReward\n')

    gamma = 0.9
    beta = 0.1
    t = 0.25
    it = 10

    SoloLearningReached, SoloTestingReached, SoloTime, SoloBestReward = [], [], [], []
    HiveLearningReached, HiveTestingReached, HiveTime, HiveBestReward = [], [], [], []

    for repeat in range(25):
        print(f'{40 * "#"}')
        # nauka 5 osobnych agentów
        hive_q = []
        h_l_reached, h_l_data, h_l_reward = [], [], []
        for track_number, truck in enumerate(LEARNING_TRACKS):
            q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=0, t=t)
            l_reached, l_data, l_reward, q = learn(it, config, q, is_Boltzamann=True, track=track_number)
            h_l_reached.append(l_reached)
            h_l_data.append(l_data)
            h_l_reward.append(l_reward)
            hive_q.append(q)

        # nauka 1 agenta
        solo_q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=0, t=t)
        s_l_reached, s_l_data, s_l_reward, solo_q = learn(it*len(LEARNING_TRACKS), config, solo_q, is_Boltzamann=True)

        print(f'{25 * "#"}')
        s_t_reached, s_t_data, s_t_reward = test(9, config, solo_q)
        h_t_reached, h_t_data, h_t_reward = test(9, config, hive_q, hive=True)
        print(f'{25 * "#"}')
        print("Learning data:")
        print("Hive data:")
        HiveLearningReached.append(np.average(h_l_reached))
        print("Solo data:")
        SoloLearningReached.append(s_l_reached)

        print(f'{25 * "#"}')
        print("Testing data:")
        print("Hive data:")
        HiveTestingReached.append(h_t_reached)
        HiveTime.append(h_t_data)
        HiveBestReward.append(h_t_reward)
        print("Solo data:")
        SoloTestingReached.append(s_t_reached)
        SoloTime.append(s_t_data)
        SoloBestReward.append(s_t_reward)

    lines.append(
        f'{np.average(SoloLearningReached)}, {np.average(SoloTestingReached)}, '
        f'{np.average(min(SoloTime))}, {np.average(max(SoloTime))}, {np.average(SoloTime)}, {np.std(SoloTime)}, '
        f'{np.average(SoloBestReward)},'
        f'{np.average(HiveLearningReached)}, {np.average(HiveTestingReached)}, '
        f'{np.average(min(HiveTime))}, {np.average(max(HiveTime))}, {np.average(HiveTime)}, {np.std(HiveTime)}, '
        f'{np.average(HiveBestReward)}'
        f'\n')
    with open('out/QLdata_fulldata_hive_vs_solo_not_sat.csv', 'w') as f:
        for line in lines:
            f.write(line)


def test_env_impact(config):
    lines = []
    lines.append(f'Number of tracks, LearningReached, TestingReached, '
                 f'Best, Worst, Average, Std, AverageReward\n')

    gamma = 0.9
    beta = 0.1
    t = 0.25
    it = 150

    for i in range(5):
        LearningReached, TestingReached, Time, BestReward = [], [], [], []
        for repeat in range(10):
            print(f'{40 * "#"}')

            q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=0, t=t)
            l_reached = []
            for j in range(i+1):
                l_reach, l_data, l_reward, q = learn(int(it/(i+1)), config, q, is_Boltzamann=True, track=j)
                l_reached.append(np.average(l_reach))

            t_reached, t_data, t_reward = test(9, config, q)
            LearningReached.append(np.average(l_reached))
            TestingReached.append(np.average(t_reached))
            Time.append(t_data)
            BestReward.append(t_reward)

        lines.append(
            f'{i+1}, '
            f'{np.average(LearningReached)}, {np.average(TestingReached)}, '
            f'{np.average(min(Time))}, {np.average(max(Time))}, {np.average(Time)}, {np.std(Time)}, '
            f'{np.average(BestReward)}'
            f'\n')
    with open('out/QLdata_fulldata_env_impact.csv', 'w') as f:
        for line in lines:
            f.write(line)


def learnSoloAgent(config):
    gamma = 0.9
    beta = 0.1
    t = 0.25
    it = 150
    print(f'{40 * "#"}')

    q = QLearningAlgorythm([-1, 0, 1], gamma=gamma, beta=beta, epsilon=0, t=t)
    l_reached = []
    i = 3
    for j in range(i + 1):
        l_reach, l_data, l_reward, q = learn(int(it / (i + 1)), config, q, is_Boltzamann=True, track=j)
        l_reached.append(np.average(l_reach))

    t_reached, t_data, t_reward = test(9, config, q)
    q.save_Q("QLKnowledge/bestAgent.json")


if __name__ == "__main__":
    config = EnvironmentConfig()
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

    # test_params_E(config)
    # test_params_T(config)
    # test_saturation(config)
    # test_hive5_vs1(config)
    # test_env_impact(config)
    learnSoloAgent(config)
