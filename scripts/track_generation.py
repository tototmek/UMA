import math
import numpy as np


class TrackGenerator:
    def through_points(points):
        x, y = zip(*points)
        coeffs = Calculus.fit_polynomial(x, y)
        return coeffs


class Calculus:
    def fit_polynomial(x, y):
        coeffs = np.polyfit(x, y, len(x)-1)
        coeffs = list(coeffs)
        coeffs.reverse()
        return coeffs
