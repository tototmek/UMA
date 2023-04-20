#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "engine.h"

namespace py = pybind11;

PYBIND11_MODULE(engine, m) {
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<std::vector<float>&>())
        .def("step", &Simulation::step, py::arg("deltatime"),
             py::arg("cartThrust"))
        .def(
            "step_multiple",
            [](Simulation& self, float deltatime, float cartThrust,
               unsigned int steps) {
                for (unsigned int i = 0; i < steps; ++i) {
                    self.step(deltatime, cartThrust);
                }
            },
            py::arg("deltatime"), py::arg("cartThrust"), py::arg("steps"))
        .def("getCartPosition", &Simulation::getCartPosition);
}