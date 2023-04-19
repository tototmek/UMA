#include "engine.h"

#include <cmath>
#include <iostream>

static const float gravity = 0.5f;
static const float efficiency = 0.995f;

void Cart::applyForce(float f) { force += f; }

void Cart::step(float deltatime, float inclination) {
    velocity += force * deltatime;
    velocity *= efficiency;
    force = 0;
    position += (velocity * deltatime) * std::cos(inclination);
}

void Cart::reset() {
    position = 0;
    velocity = 0;
    force = 0;
}

void Simulation::step(float deltatime, float cartThrust) {
    float cartPosition = cart.getPosition();
    float inclination = getInclinationAt(cartPosition);
    float gravityX = gravity * std::cos(inclination);
    if (inclination > 0) {
        gravityX = -gravityX;
    }
    cart.applyForce(gravityX);
    cart.applyForce(cartThrust);
    cart.step(deltatime, inclination);
}

float Simulation::getInclinationAt(float x) { return inclination(x); }
