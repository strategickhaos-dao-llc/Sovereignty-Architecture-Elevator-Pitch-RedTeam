// unity/Assets/Scripts/MeetingsTask.cs
using UnityEngine;
using System;
using System.Collections.Generic;
using System.Linq;

[Serializable]
public class MeetingItem
{
    public string id;
    public string title;
    public DateTime startTime;
    public DateTime endTime;
    public string location; // "zoom", "teams", "in_person", "phone"
    public List<string> attendees;
    public string agenda;
    public List<string> prepChecklist;
}

[Serializable]
public class MeetingsContext
{
    public List<MeetingItem> meetings;
    public DateTime currentTime;
    public int prepWarningMinutes = 30;
}

[Serializable]
public class MeetingsReviewResult
{
    public MeetingItem nextMeeting;
    public List<MeetingItem> todayMeetings;
    public List<MeetingItem> needsPrep;
    public int minutesUntilNext;
    public string note;
}

public static class MeetingsAlgorithm
{
    public static MeetingsReviewResult Run(MeetingsContext ctx)
    {
        var today = ctx.currentTime.Date;
        var todayMeetings = ctx.meetings
            .Where(m => m.startTime.Date == today && m.startTime > ctx.currentTime)
            .OrderBy(m => m.startTime)
            .ToList();
        
        var nextMeeting = todayMeetings.FirstOrDefault();
        
        var prepThreshold = ctx.currentTime.AddMinutes(ctx.prepWarningMinutes);
        var needsPrep = todayMeetings
            .Where(m => m.startTime <= prepThreshold && m.prepChecklist != null && m.prepChecklist.Count > 0)
            .ToList();
        
        int minutesUntilNext = -1;
        if (nextMeeting != null)
        {
            minutesUntilNext = (int)(nextMeeting.startTime - ctx.currentTime).TotalMinutes;
        }
        
        var notes = new List<string>();
        if (needsPrep.Count > 0)
            notes.Add($"📋 {needsPrep.Count} meeting(s) need prep NOW!");
        if (nextMeeting != null)
            notes.Add($"⏰ Next: '{nextMeeting.title}' in {minutesUntilNext} min.");
        notes.Add($"📅 {todayMeetings.Count} meeting(s) remaining today.");
        
        var note = todayMeetings.Count == 0 ? "🎉 No more meetings today!" : string.Join(" ", notes);
        
        return new MeetingsReviewResult
        {
            nextMeeting = nextMeeting,
            todayMeetings = todayMeetings,
            needsPrep = needsPrep,
            minutesUntilNext = minutesUntilNext,
            note = note
        };
    }

    public static string FormatMeeting(MeetingItem meeting)
    {
        string locationEmoji = meeting.location switch
        {
            "zoom" => "📹",
            "teams" => "👥",
            "in_person" => "🏢",
            "phone" => "📞",
            _ => "📍"
        };
        
        var lines = new List<string>
        {
            $"=== {meeting.title} ===",
            $"  {locationEmoji} {meeting.location.ToUpper()}",
            $"  🕐 {meeting.startTime:HH:mm} - {meeting.endTime:HH:mm}",
            $"  👤 Attendees: {string.Join(", ", meeting.attendees)}"
        };
        
        if (!string.IsNullOrEmpty(meeting.agenda))
            lines.Add($"  📝 Agenda: {meeting.agenda}");
        
        if (meeting.prepChecklist != null && meeting.prepChecklist.Count > 0)
        {
            lines.Add("  ✅ Prep Checklist:");
            foreach (var item in meeting.prepChecklist)
                lines.Add($"     - {item}");
        }
        
        return string.Join("\n", lines);
    }

    public static string FormatDaySchedule(List<MeetingItem> meetings)
    {
        if (meetings == null || meetings.Count == 0)
            return "=== Today's Schedule ===\nNo meetings scheduled.";
        
        var lines = new List<string> { "=== Today's Schedule ===" };
        foreach (var m in meetings.OrderBy(m => m.startTime))
        {
            var duration = (int)(m.endTime - m.startTime).TotalMinutes;
            lines.Add($"  {m.startTime:HH:mm} - {m.title} ({duration} min)");
        }
        
        return string.Join("\n", lines);
    }
}
