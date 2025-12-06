// cpp/src/meetings.h
#pragma once
#include <string>
#include <vector>
#include <chrono>

struct MeetingItem {
    std::string id;
    std::string title;
    std::chrono::system_clock::time_point start_time;
    std::chrono::system_clock::time_point end_time;
    std::string location; // "zoom", "teams", "in_person", "phone"
    std::vector<std::string> attendees;
    std::string agenda;
    std::vector<std::string> prep_checklist;
    bool has_agenda = false;
    bool has_prep_checklist = false;
};

struct MeetingsContext {
    std::vector<MeetingItem> meetings;
    std::chrono::system_clock::time_point current_time;
    int prep_warning_minutes = 30;
};

struct MeetingsReviewResult {
    MeetingItem next_meeting;
    bool has_next_meeting;
    std::vector<MeetingItem> today_meetings;
    std::vector<MeetingItem> needs_prep;
    int minutes_until_next;
    std::string note;
};

class MeetingsTask {
public:
    MeetingsReviewResult run(const MeetingsContext& ctx);
    std::string format_meeting(const MeetingItem& meeting);
    std::string format_day_schedule(const std::vector<MeetingItem>& meetings);
};
