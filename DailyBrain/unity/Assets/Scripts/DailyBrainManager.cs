// unity/Assets/Scripts/DailyBrainManager.cs
using UnityEngine;
using System;

public class DailyBrainManager : MonoBehaviour
{
    [Header("Commute Settings")]
    public Coordinates home = new Coordinates { lat = 29.4241, lon = -98.4936 };
    public Coordinates work = new Coordinates { lat = 29.7604, lon = -95.3698 };

    [Header("Task Toggles")]
    public bool runCommuteTask = true;
    public bool runSleepTask = false;
    public bool runReviewTasks = false;
    public bool runMeetingsTask = false;

    void Start()
    {
        // Fake a "start of day"
        DateTime departure = DateTime.Now;

        if (runCommuteTask)
        {
            var ctx = new CommuteContext
            {
                home = home,
                work = work,
                departureTime = departure
            };

            var result = CommuteAlgorithm.EstimateCommute(ctx);
            Debug.Log("=== Commute (Unity) ===");
            Debug.Log(result.note);
        }

        // TODO:
        // if (runSleepTask) RunSleepTask();
        // if (runReviewTasks) RunReviewTasks();
        // if (runMeetingsTask) RunMeetingsTask();
    }
}
