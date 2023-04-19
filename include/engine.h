#include <functional>
#include <map>
#include <vector>

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
    using Func = std::function<float(float)>;
    Cart cart;
    Func inclination;

   public:
    Simulation(Func inclinationFunc) : inclination(inclinationFunc){};
    void setInclination(Func inclinationFunc) { inclination = inclinationFunc; }
    void step(float deltatime, float cartThrust);
    float getCartPosition() { return cart.getPosition(); }
    float getInclinationAt(float x);
    void reset() { cart.reset(); }
};