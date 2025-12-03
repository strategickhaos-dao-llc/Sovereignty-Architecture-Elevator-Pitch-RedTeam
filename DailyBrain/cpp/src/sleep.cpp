// cpp/src/sleep.cpp
#include "sleep.h"
#include <iostream>
#include <iomanip>
#include <sstream>

SleepResult SleepTask::run(const SleepContext& ctx) {
    std::time_t time_t_val = std::chrono::system_clock::to_time_t(ctx.current_time);
    std::tm current_tm = *std::localtime(&time_t_val);
    
    int current_minutes = current_tm.tm_hour * 60 + current_tm.tm_min;
    int target_minutes = ctx.target_bedtime_hour * 60 + ctx.target_bedtime_minute;
    
    // Handle midnight crossing: if target is smaller than current,
    // it means bedtime is after midnight (e.g., target 1:00 AM, current 11:00 PM)
    int minutes_remaining;
    if (target_minutes < current_minutes) {
        // Add 24 hours worth of minutes for next-day bedtime
        minutes_remaining = (24 * 60 - current_minutes) + target_minutes;
    } else {
        minutes_remaining = target_minutes - current_minutes;
    }
    
    SleepResult result;
    
    if (minutes_remaining <= 0) {
        result.should_initiate = true;
        result.minutes_until_shutdown = 0;
        result.note = "Bedtime reached. Initiating shutdown sequence.";
    } else if (minutes_remaining <= ctx.shutdown_warning_minutes) {
        result.should_initiate = false;
        result.minutes_until_shutdown = minutes_remaining;
        std::ostringstream oss;
        oss << "Warning: " << minutes_remaining << " minutes until bedtime.";
        result.note = oss.str();
    } else {
        result.should_initiate = false;
        result.minutes_until_shutdown = minutes_remaining;
        std::ostringstream oss;
        oss << "Bedtime in " << minutes_remaining << " minutes.";
        result.note = oss.str();
    }
    
    return result;
}

void SleepTask::log_sleep_time(const std::chrono::system_clock::time_point& sleep_time) {
    std::time_t time_t_val = std::chrono::system_clock::to_time_t(sleep_time);
    std::tm tm = *std::localtime(&time_t_val);
    
    std::cout << "[SLEEP LOG] Sleep initiated at: "
              << std::put_time(&tm, "%Y-%m-%d %H:%M") << std::endl;
}
