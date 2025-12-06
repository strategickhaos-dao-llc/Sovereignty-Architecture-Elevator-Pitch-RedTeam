// cpp/src/meetings.cpp
#include "meetings.h"
#include <algorithm>
#include <sstream>
#include <iomanip>

MeetingsReviewResult MeetingsTask::run(const MeetingsContext& ctx) {
    MeetingsReviewResult result;
    result.has_next_meeting = false;
    result.minutes_until_next = -1;
    
    // Get current date for filtering today's meetings
    std::time_t current_time_t = std::chrono::system_clock::to_time_t(ctx.current_time);
    std::tm current_tm = *std::localtime(&current_time_t);
    
    for (const auto& m : ctx.meetings) {
        std::time_t start_time_t = std::chrono::system_clock::to_time_t(m.start_time);
        std::tm start_tm = *std::localtime(&start_time_t);
        
        // Check if same day and in the future
        if (start_tm.tm_year == current_tm.tm_year &&
            start_tm.tm_yday == current_tm.tm_yday &&
            m.start_time > ctx.current_time) {
            result.today_meetings.push_back(m);
        }
    }
    
    // Sort by start time
    std::sort(result.today_meetings.begin(), result.today_meetings.end(),
              [](const MeetingItem& a, const MeetingItem& b) {
                  return a.start_time < b.start_time;
              });
    
    // Set next meeting
    if (!result.today_meetings.empty()) {
        result.next_meeting = result.today_meetings[0];
        result.has_next_meeting = true;
        
        auto diff = result.next_meeting.start_time - ctx.current_time;
        result.minutes_until_next = static_cast<int>(
            std::chrono::duration_cast<std::chrono::minutes>(diff).count()
        );
    }
    
    // Find meetings needing prep
    auto prep_threshold = ctx.current_time + std::chrono::minutes(ctx.prep_warning_minutes);
    for (const auto& m : result.today_meetings) {
        if (m.start_time <= prep_threshold && m.has_prep_checklist) {
            result.needs_prep.push_back(m);
        }
    }
    
    // Generate note
    std::ostringstream oss;
    if (!result.needs_prep.empty()) {
        oss << "📋 " << result.needs_prep.size() << " meeting(s) need prep NOW! ";
    }
    if (result.has_next_meeting) {
        oss << "⏰ Next: '" << result.next_meeting.title
            << "' in " << result.minutes_until_next << " min. ";
    }
    oss << "📅 " << result.today_meetings.size() << " meeting(s) remaining today.";
    
    result.note = result.today_meetings.empty() ?
                  "🎉 No more meetings today!" : oss.str();
    
    return result;
}

std::string MeetingsTask::format_meeting(const MeetingItem& meeting) {
    std::string location_emoji;
    if (meeting.location == "zoom") location_emoji = "📹";
    else if (meeting.location == "teams") location_emoji = "👥";
    else if (meeting.location == "in_person") location_emoji = "🏢";
    else if (meeting.location == "phone") location_emoji = "📞";
    else location_emoji = "📍";
    
    std::time_t start_t = std::chrono::system_clock::to_time_t(meeting.start_time);
    std::time_t end_t = std::chrono::system_clock::to_time_t(meeting.end_time);
    std::tm start_tm = *std::localtime(&start_t);
    std::tm end_tm = *std::localtime(&end_t);
    
    std::ostringstream oss;
    oss << "=== " << meeting.title << " ===" << std::endl;
    oss << "  " << location_emoji << " " << meeting.location << std::endl;
    oss << "  🕐 " << std::put_time(&start_tm, "%H:%M")
        << " - " << std::put_time(&end_tm, "%H:%M") << std::endl;
    
    oss << "  👤 Attendees: ";
    for (size_t i = 0; i < meeting.attendees.size(); ++i) {
        if (i > 0) oss << ", ";
        oss << meeting.attendees[i];
    }
    oss << std::endl;
    
    if (meeting.has_agenda) {
        oss << "  📝 Agenda: " << meeting.agenda << std::endl;
    }
    
    if (meeting.has_prep_checklist) {
        oss << "  ✅ Prep Checklist:" << std::endl;
        for (const auto& item : meeting.prep_checklist) {
            oss << "     - " << item << std::endl;
        }
    }
    
    return oss.str();
}

std::string MeetingsTask::format_day_schedule(const std::vector<MeetingItem>& meetings) {
    if (meetings.empty()) {
        return "=== Today's Schedule ===\nNo meetings scheduled.";
    }
    
    std::ostringstream oss;
    oss << "=== Today's Schedule ===" << std::endl;
    
    for (const auto& m : meetings) {
        std::time_t start_t = std::chrono::system_clock::to_time_t(m.start_time);
        std::tm start_tm = *std::localtime(&start_t);
        
        auto duration_mins = std::chrono::duration_cast<std::chrono::minutes>(
            m.end_time - m.start_time).count();
        
        oss << "  " << std::put_time(&start_tm, "%H:%M")
            << " - " << m.title << " (" << duration_mins << " min)" << std::endl;
    }
    
    return oss.str();
}
