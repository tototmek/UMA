#include "track.h"

#include <cmath>

Track::Track(Coeffs& coeffs) {
    elevationMap = generateElevation(coeffs);
    slopeMap = generateSlope(coeffs);
}

Track::Func Track::generateElevation(Coeffs& coeffs) {
    return [coeffs](float x) {
        float result = 0;
        for (size_t i = 0; i < coeffs.size(); ++i) {
            result += coeffs[i] * std::pow(x, i);
        }
        return result;
    };
}

Track::Func Track::generateSlope(Coeffs& coeffs) {
    return [coeffs](float x) {
        float result = 0;
        for (size_t i = 1; i < coeffs.size(); ++i) {
            result += coeffs[i] * i * std::pow(x, i - 1);
        }
        return result;
    };
}