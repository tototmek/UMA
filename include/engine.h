#include <functional>
#include <map>
#include <vector>

#include "track.h"

class Cart {
   private:
    float position, velocity, force;

   public:
    float getPosition() { return position; }
    void applyForce(float f);
    void step(float deltatime, float inclination);
    void reset();
};

class Simulation {
   private:
    Cart cart;
    Track track;

   public:
    Simulation(std::vector<float>& c) : track(c){};
    void step(float deltatime, float cartThrust);
    float getCartPosition() { return cart.getPosition(); }
    float getInclinationAt(float x);
    void reset() { cart.reset(); }
};