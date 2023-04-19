#include "engine.h"

#include <cmath>

static const float gravity = 9.81f;

void Cart::step(float deltatime) {
    velocity += force * deltatime;
    force = 0;
    position += velocity * deltatime;
}

void Simulation::step(float deltatime, float cartThrust) {
    float cartPosition = cart.getPosition();
    float inclination = getInclinationAt(cartPosition);
    float gravityX = gravity * std::sin(inclination);
    cart.applyForce(gravityX);
    cart.applyForce(cartThrust);
    cart.step(deltatime);
}

Simulation::Simulation() {
    inclinationMap = [](float x) {
        (void)x;
        return 0.0f;
    };
}

float Simulation::getInclinationAt(float x) { return inclinationMap(x); }

#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(engine, m) {
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<>())
        .def("step", &Simulation::step)
        .def("getCartPosition", &Simulation::getCartPosition);
}