// unity/Assets/Scripts/CommuteTask.cs
using UnityEngine;
using System;

[Serializable]
public class Coordinates
{
    public double lat;
    public double lon;
}

[Serializable]
public class CommuteContext
{
    public Coordinates home;
    public Coordinates work;
    public DateTime departureTime;
}

[Serializable]
public class CommuteResult
{
    public TimeSpan estimatedDuration;
    public DateTime eta;
    public string note;
}

public static class CommuteAlgorithm
{
    public static CommuteResult EstimateCommute(CommuteContext ctx)
    {
        double distanceKm = Haversine(ctx.home, ctx.work);
        double hours = distanceKm / 40.0;
        TimeSpan duration = TimeSpan.FromHours(hours);
        DateTime eta = ctx.departureTime + duration;

        string note = $"Distance ~{distanceKm:F1} km, ETA at {eta:HH:mm}.";

        return new CommuteResult
        {
            estimatedDuration = duration,
            eta = eta,
            note = note
        };
    }

    private static double Haversine(Coordinates a, Coordinates b)
    {
        const double R = 6371.0;
        double Deg2Rad(double d) => d * Math.PI / 180.0;

        double dlat = Deg2Rad(b.lat - a.lat);
        double dlon = Deg2Rad(b.lon - a.lon);
        double lat1 = Deg2Rad(a.lat);
        double lat2 = Deg2Rad(b.lat);

        double h = Math.Sin(dlat / 2) * Math.Sin(dlat / 2) +
                   Math.Cos(lat1) * Math.Cos(lat2) *
                   Math.Sin(dlon / 2) * Math.Sin(dlon / 2);

        return 2 * R * Math.Asin(Math.Sqrt(h));
    }
}
