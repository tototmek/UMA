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


def data_run(maxIter, algorithm, is_testing=False):
    start_time = time.time()
    data = []
    running = True
    environment.reset()
    iter = 1
    reached = 0
    last_reached = 0

    velocity, inclination, inclination_ahead, reward, is_terminal = environment.step(0)
    start_state = [round(velocity), round(inclination), round(inclination_ahead)]
    old_state = start_state
    algorithm.make_Q(old_state)

    while running:
        action = algorithm.make_move(old_state)
        if action == 1:
            thrust = 1.0
        elif action == 0:
            thrust = 0.0
        else:
            thrust = -1.0

        velocity, inclination, inclination_ahead, reward, is_terminal = environment.step(thrust)
        new_state = [round(velocity), round(inclination), round(inclination_ahead)]
        algorithm.make_Q(new_state)

        if is_testing:
            algorithm.default_learning(new_state, is_terminal, old_state, action, round(reward, 1))
            old_state = new_state

        if is_terminal:
            reached += 1
            diff = iter-last_reached
            data.append(diff)

            last_reached = iter

            environment.reset()
            old_state = start_state

            print(f"Target reached in {diff} iterations")
            if iter > maxIter:
                running = False
                if is_testing:
                    print("Learning complied")
                else:
                    print("Testing complied")
        iter += 1
    print(f'Time: {round(time.time() - start_time, 2)}[s]')
    return reached, data

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

lines = []
lines.append(f'Gamma, Beta, Epsilon, Reached, Best, Worst, Average, Std\n')
if __name__ == "__main__":
    q = QLearningAlgorythm([-1, 0, 1], 0.9, 0.9, 0.25)
    l_reached, l_data = data_run(100000, q, is_testing=True)
    print(f'{25 * "#"}')
    t_reached, t_data = data_run(10000, q)
    print(f'{25*"#"}')
    print("Learning data:")
    print(f"Reached targets: {l_reached}")
    print(f"Best time: {min(l_data)}")
    print(f"Worst time: {max(l_data)}")
    print(f"Avg time: {np.average(l_data)}")
    print(f"Std: {np.std(l_data)}")
    print(f'{25 * "#"}')
    t_min = min(t_data)
    t_max = max(t_data)
    t_avg = np.average(t_data)
    t_std = np.std(t_data)
    print("Testing data:")
    print(f"Reached targets: {t_reached}")
    print(f"Best time: {t_min}")
    print(f"Worst time: {t_max}")
    print(f"Avg time: {t_avg}")
    print(f"Std: {t_std}")
    lines.append(f'{q.gamma}, {q.beta}, {q.epsilon}, {t_reached}, {t_reached}, {t_min}, {t_max}, {t_avg}, {t_std}\n')
    with open('out/QLdata.csv', 'w') as f:
        for line in lines:
            f.write(line)
