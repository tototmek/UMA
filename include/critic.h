#pragma once
#ifndef CRITIC_H
#define CRITIC_H
#include <memory>

#include "engine.h"

namespace critic {

using Reward = std::function<float(const Simulation&)>;
using Rewards = std::vector<std::pair<Reward, float>>;

class Critic {
   private:
    Rewards rewards;

   public:
    Critic(Rewards r) : rewards(r){};
    float getReward(const Simulation& sim);
};

namespace rewards {

Reward makePositionReward();
Reward makeVelocityReward(float targetVelocity);
Reward makeTimePenalty();
Reward makeReversingPenalty();
Reward makeOverspeedPenalty(float maxVelocity);

}  // namespace rewards
}  // namespace critic

#endif