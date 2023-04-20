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
    void step(float deltatime);
    void reset();
};

class Simulation {
   private:
    Cart cart;
    Track track;

   public:
    Simulation(std::vector<float>& c) : track(c){};
    void step(float deltatime, float cartThrust);
    float getInclinationAt(float x);
    void reset() { cart.reset(); }
    Cart& getCart() { return cart; }
    Track& getTrack() { return track; }
};