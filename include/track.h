#include <functional>
#include <vector>

namespace track {

using Func = std::function<float(float)>;
using Coeffs = std::vector<float>;
using Point = std::pair<float, float>;
using Splines = std::vector<std::pair<Point, Coeffs>>;

class Track {
   private:
    Func elevationMap;
    Func slopeMap;

    Func generateElevation(Splines c);
    Func generateSlope(Splines c);

   public:
    Track(std::vector<Point>& points);
    float slopeAt(float x) { return slopeMap(x); }
    Func& getSlopeMap() { return slopeMap; }
    Func& getElevationMap() { return elevationMap; }
};

class TrackGenerator {
   public:
    static Splines generateSplines(std::vector<Point>& points);
    static Coeffs calculateSplineCoeffs(Point& point1, Point& point2);
    static Coeffs findSplineCoeffsAt(float x, Splines splines);
};

}  // namespace track
