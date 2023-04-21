#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#include "critic.h"
#include "engine.h"
#include "track.h"

struct EnvironmentConfig {
    std::vector<track::Point> points;
    float trackLength;
    float gravity;
    float efficiency;
    float simDeltatime;
    int simStepsPerStep;
    float inclinationLookAheadDistance;
    float positionRewardGain;
    float velocityRewardGain;
    float timePenaltyGain;
    float reversingPenaltyGain;
    float overspeedPenaltyGain;
    float finishRewardGain;
    float targetVelocity;
    float maxVelocity;
};

struct StepInput {
    float action;
};

struct StepOutput {
    float velocity;
    float inclination;
    float inclinationAhead;
    float reward;
    bool isTerminal;
};

critic::Rewards rewardsFromConfig(const EnvironmentConfig& c);

class Environment {
   private:
    Simulation simulation;
    critic::Critic critic;
    const EnvironmentConfig config;

    void executeSteps(StepInput& in);
    StepOutput buildOutput();

   public:
    Environment(const EnvironmentConfig& c)
        : simulation(c.points, c.gravity, c.efficiency),
          critic(rewardsFromConfig(c)),
          config(c){};
    StepOutput step(StepInput& in);
    const Simulation& getSimulation() const { return simulation; };
};

#endif