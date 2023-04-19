#include <functional>
#include <vector>

int add(int, int);

class Cart {
   private:
    float position, velocity, force;

   public:
    float getPosition() { return position; }
    void applyForce(float f) { force += f; }
    void step(float deltatime);
};

class Simulation {
   private:
    Cart cart;
    std::function<float(float)> inclinationMap;
    float getInclinationAt(float x);

   public:
    Simulation();
    void step(float deltatime, float cartThrust);
    float getCartPosition() { return cart.getPosition(); }
};