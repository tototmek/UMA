#pragma once
#ifndef ENGINE_H
#define ENGINE_H
#include <functional>
#include <map>
#include <vector>

#include "track.h"

namespace engine {

static float gravity = 18.0f;
static float efficiency = 0.99f;

class Cart {
   private:
    float position, velocity, force;

   public:
    float getPosition() const { return position; }
    float getVelocity() const { return velocity; }
    void applyForce(float f);
    void step(float deltatime, float inclination);
    void reset();
};

class Simulation {
   private:
    Cart cart;
    track::Track track;

   public:
    Simulation(const std::vector<track::Point>& c) : track(c){};
    Simulation(const std::vector<track::Point>& c, float g, float e)
        : track(c) {
        gravity = g;
        efficiency = e;
    };
    void step(float deltatime, float cartThrust);
    float getInclinationAt(float x);
    void reset() { cart.reset(); }
    const Cart& getCart() const { return cart; }
    const track::Track& getTrack() const { return track; }
};

}  // namespace engine

#endif