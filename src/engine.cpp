#include "engine.h"

#include <cmath>
#include <iostream>

static const float gravity = 9.81f;
static const float efficiency = 0.996f;

void Cart::applyForce(float f) { force += f; }

void Cart::step(float deltatime, float inclination) {
    velocity += force * deltatime;
    velocity *= efficiency;
    force = 0;
    position += (velocity * deltatime) * std::cos(inclination);
    (void)inclination;
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
    // std::cout << "Inclination: " << inclination
    //           << "\tcos(Inclination): " << std::cos(inclination)
    //           << "\tGravityX: " << gravityX << std::endl;
}

float Simulation::getInclinationAt(float x) {
    return std::atan(track.slopeAt(x));
}
