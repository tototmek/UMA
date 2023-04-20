#include <functional>
#include <vector>

class Track {
   private:
    using Func = std::function<float(float)>;
    using Coeffs = std::vector<float>;
    Func elevationMap;
    Func slopeMap;

    Func generateElevation(Coeffs& c);
    Func generateSlope(Coeffs& c);

   public:
    Track(Coeffs& c);
    float slopeAt(float x) { return slopeMap(x); }
    Func& getSlopeMap() { return slopeMap; }
    Func& getElevationMap() { return elevationMap; }
};
