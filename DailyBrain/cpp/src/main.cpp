// cpp/src/main.cpp
#include "commute.h"
#include <iostream>
#include <chrono>

int main() {
    Coordinates home{29.4241, -98.4936};
    Coordinates work{29.7604, -95.3698};

    CommuteContext ctx{
        home,
        work,
        std::chrono::system_clock::now()
    };

    CommuteAlgorithm algo;
    CommuteResult result = algo.estimate_commute(ctx);

    std::cout << "=== Commute (C++) ===\n";
    std::cout << result.note << "\n";
    std::cout << "Duration (secs): " << result.estimated_duration.count() << "\n";

    // TODO: call SleepTask, ReviewTasks, MeetingsTask...
    return 0;
}
