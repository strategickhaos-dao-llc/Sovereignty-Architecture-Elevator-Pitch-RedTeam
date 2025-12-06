// cpp/src/commute.cpp
#include "commute.h"
#include <cmath>
#include <sstream>
#include <iomanip>

double CommuteAlgorithm::haversine(const Coordinates& a, const Coordinates& b) {
    static const double R = 6371.0; // km
    auto deg2rad = [](double d) { return d * M_PI / 180.0; };

    double dlat = deg2rad(b.lat - a.lat);
    double dlon = deg2rad(b.lon - a.lon);
    double lat1 = deg2rad(a.lat);
    double lat2 = deg2rad(b.lat);

    double h = std::sin(dlat / 2) * std::sin(dlat / 2)
             + std::cos(lat1) * std::cos(lat2)
             * std::sin(dlon / 2) * std::sin(dlon / 2);

    return 2 * R * std::asin(std::sqrt(h));
}

CommuteResult CommuteAlgorithm::estimate_commute(const CommuteContext& ctx) {
    double distance_km = haversine(ctx.home, ctx.work);
    double hours = distance_km / 40.0;
    auto secs = std::chrono::seconds(static_cast<int>(hours * 3600.0));

    auto eta = ctx.departure_time + secs;

    std::time_t eta_time_t = std::chrono::system_clock::to_time_t(eta);
    std::tm tm = *std::localtime(&eta_time_t);

    std::ostringstream oss;
    oss << "Distance ~" << std::fixed << std::setprecision(1)
        << distance_km << " km, ETA at "
        << std::setfill('0') << std::setw(2) << tm.tm_hour << ":"
        << std::setfill('0') << std::setw(2) << tm.tm_min;

    CommuteResult result;
    result.estimated_duration = secs;
    result.eta = eta;
    result.note = oss.str();
    return result;
}
