// cpp/src/sleep.h
#pragma once
#include <string>
#include <chrono>

struct SleepContext {
    int target_bedtime_hour;
    int target_bedtime_minute;
    std::chrono::system_clock::time_point current_time;
    int shutdown_warning_minutes = 30;
};

struct SleepResult {
    bool should_initiate;
    int minutes_until_shutdown;
    std::string note;
};

class SleepTask {
public:
    SleepResult run(const SleepContext& ctx);
    void log_sleep_time(const std::chrono::system_clock::time_point& sleep_time);
};
