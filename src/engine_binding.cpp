#include <pybind11/functional.h>
#include <pybind11/pybind11.h>

#include "engine.h"

namespace py = pybind11;

PYBIND11_MODULE(engine, m) {
    py::class_<Simulation>(m, "Simulation")
        .def(py::init<std::function<float(float)>>(),
             py::arg("track_inclination"))
        .def("setInclination", &Simulation::setInclination)
        .def("step", &Simulation::step)
        .def("getCartPosition", &Simulation::getCartPosition);
}