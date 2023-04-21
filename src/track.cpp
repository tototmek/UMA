#include "track.h"

#include <cmath>
#include <iostream>
#include <stdexcept>
using namespace track;

Track::Track(const std::vector<Point>& points) {
    Splines splines = TrackGenerator::generateSplines(points);

    elevationMap = generateElevation(splines);
    slopeMap = generateSlope(splines);
}

Func Track::generateElevation(const Splines& splines) {
    return [splines](float x) {
        Coeffs coeffs = TrackGenerator::findSplineCoeffsAt(x, splines);
        float result = 0;
        for (size_t i = 0; i < coeffs.size(); ++i) {
            result += coeffs[i] * std::pow(x, i);
        }
        return result;
    };
}

Func Track::generateSlope(const Splines& splines) {
    return [splines](float x) {
        Coeffs coeffs = TrackGenerator::findSplineCoeffsAt(x, splines);
        float result = 0;
        for (size_t i = 1; i < coeffs.size(); ++i) {
            result += coeffs[i] * i * std::pow(x, i - 1);
        }
        return result;
    };
}

Coeffs TrackGenerator::calculateSplineCoeffs(const Point& point1,
                                             const Point& point2) {
    const auto [x1, y1] = point1;
    const auto [x2, y2] = point2;
    float a0, a1, a2, a3;

    a0 = ((x1 * x1 * x1) * y2 - (x2 * x2 * x2) * y1 +
          x1 * (x2 * x2) * y1 * 3.0 - (x1 * x1) * x2 * y2 * 3.0) /
         ((x1 - x2) * (x1 * x2 * -2.0 + x1 * x1 + x2 * x2));
    a1 = ((x1 * x2 * y1 - x1 * x2 * y2) * -6.0) /
         (x1 * (x2 * x2) * 3.0 - (x1 * x1) * x2 * 3.0 + x1 * x1 * x1 -
          x2 * x2 * x2);
    a2 = ((x1 + x2) * (y1 - y2) * 3.0) /
         (x1 * (x2 * x2) * 3.0 - (x1 * x1) * x2 * 3.0 + x1 * x1 * x1 -
          x2 * x2 * x2);
    a3 = ((y1 - y2) * -2.0) / (x1 * (x2 * x2) * 3.0 - (x1 * x1) * x2 * 3.0 +
                               x1 * x1 * x1 - x2 * x2 * x2);

    return {a0, a1, a2, a3};
}

Coeffs TrackGenerator::findSplineCoeffsAt(float x, const Splines& splines) {
    if (x < splines[0].first.first) {
        return splines[0].second;
    }
    if (x >= splines[splines.size() - 1].first.second) {
        return splines[splines.size() - 1].second;
    }

    for (const auto spline : splines) {
        auto& [limits, coeffs] = spline;
        if (x >= limits.first && x < limits.second) {
            return coeffs;
        }
    }
    throw std::domain_error("Spline not found. Very weird...");
}

Splines TrackGenerator::generateSplines(const std::vector<Point>& points) {
    Splines splines;
    for (size_t i = 1; i < points.size(); ++i) {
        Coeffs splineCoeffs = TrackGenerator::calculateSplineCoeffs(
            points.at(i - 1), points.at(i));

        std::pair<float, float> splineLimits = {points[i - 1].first,
                                                points[i].first};

        splines.push_back({splineLimits, splineCoeffs});
    }
    return splines;
}