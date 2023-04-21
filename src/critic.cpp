#include "critic.h"

using namespace critic;
using namespace engine;

float Critic::getReward(const Simulation& sim) {
    float result = 0.0f;
    for (const auto& reward : rewards) {
        auto& [function, weight] = reward;
        result += weight * function(sim);
    }
    return result;
}

Reward rewards::makePositionReward() {
    return [](const Simulation& sim) {
        static float prevPosition = 0.0f;
        float currentPosition = sim.getCart().getPosition();
        float reward = currentPosition - prevPosition;
        prevPosition = currentPosition;
        return reward;
    };
}

Reward rewards::makeVelocityReward(float targetVelocity) {
    return [targetVelocity](const Simulation& sim) {
        float currentVelocity = sim.getCart().getVelocity();
        return -std::abs(targetVelocity - currentVelocity);
    };
}

Reward rewards::makeTimePenalty() {
    return [](const Simulation& sim) {
        (void)sim;
        return -1.0f;
    };
}

Reward rewards::makeReversingPenalty() {
    return [](const Simulation& sim) {
        float velocity = sim.getCart().getVelocity();
        return -1.0f ? (velocity < 0) : 0.0f;
    };
}

Reward rewards::makeOverspeedPenalty(float maxVelocity) {
    return [maxVelocity](const Simulation& sim) {
        float velocity = sim.getCart().getVelocity();
        bool isOverspeed = (velocity > maxVelocity || velocity < -maxVelocity);
        return -1.0f ? isOverspeed : 0.0f;
    };
}