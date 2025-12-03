// unity/Assets/Scripts/SleepTask.cs
using UnityEngine;
using System;

[Serializable]
public class SleepContext
{
    public int targetBedtimeHour;
    public int targetBedtimeMinute;
    public DateTime currentTime;
    public int shutdownWarningMinutes = 30;
}

[Serializable]
public class SleepResult
{
    public bool shouldInitiate;
    public int minutesUntilShutdown;
    public string note;
}

public static class SleepAlgorithm
{
    public static SleepResult Run(SleepContext ctx)
    {
        int currentMinutes = ctx.currentTime.Hour * 60 + ctx.currentTime.Minute;
        int targetMinutes = ctx.targetBedtimeHour * 60 + ctx.targetBedtimeMinute;
        
        // Handle midnight crossing: if target is smaller than current,
        // it means bedtime is after midnight (e.g., target 1:00 AM, current 11:00 PM)
        int minutesRemaining;
        if (targetMinutes < currentMinutes)
        {
            // Add 24 hours worth of minutes for next-day bedtime
            minutesRemaining = (24 * 60 - currentMinutes) + targetMinutes;
        }
        else
        {
            minutesRemaining = targetMinutes - currentMinutes;
        }
        
        if (minutesRemaining <= 0)
        {
            return new SleepResult
            {
                shouldInitiate = true,
                minutesUntilShutdown = 0,
                note = "Bedtime reached. Initiating shutdown sequence."
            };
        }
        else if (minutesRemaining <= ctx.shutdownWarningMinutes)
        {
            return new SleepResult
            {
                shouldInitiate = false,
                minutesUntilShutdown = minutesRemaining,
                note = $"Warning: {minutesRemaining} minutes until bedtime."
            };
        }
        else
        {
            return new SleepResult
            {
                shouldInitiate = false,
                minutesUntilShutdown = minutesRemaining,
                note = $"Bedtime in {minutesRemaining} minutes."
            };
        }
    }

    public static void LogSleepTime(DateTime sleepTime)
    {
        Debug.Log($"[SLEEP LOG] Sleep initiated at: {sleepTime:yyyy-MM-dd HH:mm}");
    }
}
