#pragma once
#ifndef ENGINE_H
#define ENGINE_H
#include <functional>
#include <map>
#include <vector>

#include "track.h"

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
    Simulation(std::vector<track::Point>& c) : track(c){};
    void step(float deltatime, float cartThrust);
    float getInclinationAt(float x);
    void reset() { cart.reset(); }
    const Cart& getCart() const { return cart; }
    const track::Track& getTrack() const { return track; }
};

#endif