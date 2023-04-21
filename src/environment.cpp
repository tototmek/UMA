#include "environment.h"

critic::Rewards rewardsFromConfig(const EnvironmentConfig& c) {
    using namespace critic::rewards;
    return {{makePositionReward(), c.positionRewardGain},
            {makeVelocityReward(c.targetVelocity), c.velocityRewardGain},
            {makeTimePenalty(), c.timePenaltyGain},
            {makeReversingPenalty(), c.reversingPenaltyGain},
            {makeOverspeedPenalty(c.maxVelocity), c.overspeedPenaltyGain}};
}

StepOutput Environment::step(const StepInput& input) {
    executeSteps(input);
    return buildOutput();
}

void Environment::executeSteps(const StepInput& in) {
    for (int i = 0; i < config.simStepsPerStep; ++i) {
        simulation.step(config.simDeltatime, in.action * config.cartThrustGain);
    }
}

StepOutput Environment::buildOutput() {
    StepOutput output;
    float position = simulation.getCart().getPosition();
    float velocity = simulation.getCart().getVelocity();
    output.velocity = velocity;
    output.inclination = simulation.getInclinationAt(position);
    output.inclinationAhead = simulation.getInclinationAt(
        position + config.inclinationLookAheadDistance);
    if (position >= config.trackLength) {
        output.reward = config.finishRewardGain;
        output.isTerminal = true;
    } else {
        output.reward = critic.getReward(simulation);
        output.isTerminal = false;
    }
    return output;
}
