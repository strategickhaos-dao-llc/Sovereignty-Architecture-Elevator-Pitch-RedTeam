// cpp/src/commute.h
#pragma once
#include <string>
#include <chrono>

struct Coordinates {
    double lat;
    double lon;
};

struct CommuteContext {
    Coordinates home;
    Coordinates work;
    std::chrono::system_clock::time_point departure_time;
};

struct CommuteResult {
    std::chrono::seconds estimated_duration;
    std::chrono::system_clock::time_point eta;
    std::string note;
};

class CommuteAlgorithm {
public:
    CommuteResult estimate_commute(const CommuteContext& ctx);

private:
    double haversine(const Coordinates& a, const Coordinates& b);
};
