#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "environment.h"

namespace py = pybind11;

PYBIND11_MODULE(environment, m) {
    py::class_<EnvironmentConfig>(m, "EnvironmentConfig")
        .def(py::init<>())
        .def_readwrite("points", &EnvironmentConfig::points)
        .def_readwrite("trackLength", &EnvironmentConfig::trackLength)
        .def_readwrite("cartThrustGain", &EnvironmentConfig::cartThrustGain)
        .def_readwrite("gravity", &EnvironmentConfig::gravity)
        .def_readwrite("efficiency", &EnvironmentConfig::efficiency)
        .def_readwrite("simDeltatime", &EnvironmentConfig::simDeltatime)
        .def_readwrite("simStepsPerStep", &EnvironmentConfig::simStepsPerStep)
        .def_readwrite("inclinationLookAheadDistance",
                       &EnvironmentConfig::inclinationLookAheadDistance)
        .def_readwrite("positionRewardGain",
                       &EnvironmentConfig::positionRewardGain)
        .def_readwrite("velocityRewardGain",
                       &EnvironmentConfig::velocityRewardGain)
        .def_readwrite("timePenaltyGain", &EnvironmentConfig::timePenaltyGain)
        .def_readwrite("reversingPenaltyGain",
                       &EnvironmentConfig::reversingPenaltyGain)
        .def_readwrite("overspeedPenaltyGain",
                       &EnvironmentConfig::overspeedPenaltyGain)
        .def_readwrite("finishRewardGain", &EnvironmentConfig::finishRewardGain)
        .def_readwrite("targetVelocity", &EnvironmentConfig::targetVelocity)
        .def_readwrite("maxVelocity", &EnvironmentConfig::maxVelocity);

    py::class_<Environment>(m, "Environment")
        .def(py::init<const EnvironmentConfig&>())
        .def("reset", &Environment::reset)
        .def("step",
             [](Environment& self, float action) {
                 auto output = self.step({action});
                 std::tuple outputTuple{output.velocity, output.inclination,
                                        output.inclinationAhead, output.reward,
                                        output.isTerminal};
                 return outputTuple;
             })
        .def("get_cart_position",
             [](Environment& self) {
                 return self.getSimulation().getCart().getPosition();
             })
        .def("get_track_elevation",
             [](Environment& self) {
                 return self.getSimulation().getTrack().getElevationMap();
             })
        .def("get_track_slope", [](Environment& self) {
            return self.getSimulation().getTrack().getSlopeMap();
        });
}
