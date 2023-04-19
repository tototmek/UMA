#include "engine.h"

#include <cmath>
#include <iostream>

static const float gravity = 9.81f;

void Cart::step(float deltatime) {
    velocity += force * deltatime;
    force = 0;
    position += velocity * deltatime;
}

void Cart::reset() {
    position = 0;
    velocity = 0;
    force = 0;
}

void Simulation::step(float deltatime, float cartThrust) {
    float cartPosition = cart.getPosition();
    float inclination = getInclinationAt(cartPosition);
    float gravityX = gravity * std::sin(inclination);
    cart.applyForce(gravityX);
    cart.applyForce(cartThrust);
    cart.step(deltatime);
    std::cout << "Inclination: " << inclination << "\n";
    std::cout << "GravityX: " << gravityX << "\n";
}

float Simulation::getInclinationAt(float x) { return inclination(x); }
