import math
import numpy as np


class Track:
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.elevation = self._calculate_elevation_function()
        self.slope = self._calculate_slope_function()

    def _calculate_elevation_function(self):
        return lambda x: sum([a * math.pow(x, i) for i, a in enumerate(self.coeffs)])

    def _calculate_slope_function(self):
        return lambda x: sum([a * (i+1) * math.pow(x, i) for i, a in enumerate(self.coeffs[1:])])

    def through_points(points):
        x, y = zip(*points)
        coeffs = Calculus.fit_polynomial(x, y)
        return Track(coeffs)


class Calculus:
    def fit_polynomial(x, y):
        coeffs = np.polyfit(x, y, len(x)-1)
        coeffs = list(coeffs)
        coeffs.reverse()
        return coeffs
