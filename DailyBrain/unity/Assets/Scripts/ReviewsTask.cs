// unity/Assets/Scripts/ReviewsTask.cs
using UnityEngine;
using System;
using System.Collections.Generic;
using System.Linq;

// ============ Homework Review ============

[Serializable]
public class HomeworkItem
{
    public string id;
    public string title;
    public string subject;
    public DateTime dueDate;
    public string status; // "not_started", "in_progress", "completed"
    public int priority;  // 1 = highest
}

[Serializable]
public class HomeworkContext
{
    public List<HomeworkItem> items;
    public DateTime currentDate;
    public int maxPriorities = 3;
}

[Serializable]
public class HomeworkReviewResult
{
    public List<HomeworkItem> overdue;
    public List<HomeworkItem> dueToday;
    public List<HomeworkItem> upcoming;
    public List<HomeworkItem> topPriorities;
    public string note;
}

public static class ReviewHomeworkAlgorithm
{
    public static HomeworkReviewResult Run(HomeworkContext ctx)
    {
        var incomplete = ctx.items.Where(h => h.status != "completed").ToList();
        
        var overdue = incomplete.Where(h => h.dueDate.Date < ctx.currentDate.Date).ToList();
        var dueToday = incomplete.Where(h => h.dueDate.Date == ctx.currentDate.Date).ToList();
        var upcoming = incomplete.Where(h => h.dueDate.Date > ctx.currentDate.Date).ToList();
        
        var topPriorities = incomplete
            .OrderBy(h => h.priority)
            .ThenBy(h => h.dueDate)
            .Take(ctx.maxPriorities)
            .ToList();
        
        var notes = new List<string>();
        if (overdue.Count > 0)
            notes.Add($"⚠️ {overdue.Count} OVERDUE item(s)!");
        if (dueToday.Count > 0)
            notes.Add($"📅 {dueToday.Count} item(s) due TODAY.");
        if (upcoming.Count > 0)
            notes.Add($"📋 {upcoming.Count} upcoming item(s).");
        
        var note = notes.Count == 0 ? "✅ All homework complete!" : string.Join(" ", notes);
        
        return new HomeworkReviewResult
        {
            overdue = overdue,
            dueToday = dueToday,
            upcoming = upcoming,
            topPriorities = topPriorities,
            note = note
        };
    }
}

// ============ Bills Review ============

[Serializable]
public class BillItem
{
    public string id;
    public string name;
    public decimal amount;
    public DateTime dueDate;
    public string category;
    public bool isPaid;
    public bool isAutopay;
}

[Serializable]
public class BillsContext
{
    public List<BillItem> bills;
    public DateTime currentDate;
    public int warningDays = 7;
}

[Serializable]
public class BillsReviewResult
{
    public List<BillItem> overdue;
    public List<BillItem> dueSoon;
    public List<BillItem> upcoming;
    public decimal totalDueSoon;
    public string note;
}

public static class ReviewBillsAlgorithm
{
    public static BillsReviewResult Run(BillsContext ctx)
    {
        var unpaid = ctx.bills.Where(b => !b.isPaid).ToList();
        
        var overdue = unpaid.Where(b => b.dueDate.Date < ctx.currentDate.Date).ToList();
        var warningThreshold = ctx.currentDate.AddDays(ctx.warningDays);
        var dueSoon = unpaid.Where(b => 
            b.dueDate.Date >= ctx.currentDate.Date && 
            b.dueDate.Date <= warningThreshold.Date).ToList();
        var upcoming = unpaid.Where(b => b.dueDate.Date > warningThreshold.Date).ToList();
        
        var totalDueSoon = overdue.Concat(dueSoon).Sum(b => b.amount);
        
        var notes = new List<string>();
        if (overdue.Count > 0)
        {
            var totalOverdue = overdue.Sum(b => b.amount);
            notes.Add($"🚨 {overdue.Count} OVERDUE bill(s) totaling ${totalOverdue:F2}!");
        }
        if (dueSoon.Count > 0)
        {
            var totalSoon = dueSoon.Sum(b => b.amount);
            notes.Add($"⏰ {dueSoon.Count} bill(s) due within {ctx.warningDays} days (${totalSoon:F2}).");
        }
        
        var note = notes.Count == 0 ? "✅ All bills are current!" : string.Join(" ", notes);
        
        return new BillsReviewResult
        {
            overdue = overdue,
            dueSoon = dueSoon,
            upcoming = upcoming,
            totalDueSoon = totalDueSoon,
            note = note
        };
    }
}

// ============ Todos Review ============

[Serializable]
public class TodoItem
{
    public string id;
    public string title;
    public DateTime? dueDate;
    public DateTime createdDate;
    public string status;   // "pending", "in_progress", "completed", "cancelled"
    public string priority; // "low", "medium", "high", "urgent"
    public string context;  // "home", "work", "errands", "personal"
}

[Serializable]
public class TodosContext
{
    public List<TodoItem> todos;
    public DateTime currentDate;
    public string filterContext;
    public int maxDisplay = 5;
}

[Serializable]
public class TodosReviewResult
{
    public List<TodoItem> urgent;
    public List<TodoItem> today;
    public List<TodoItem> overdue;
    public List<TodoItem> nextActions;
    public string note;
}

public static class ReviewTodosAlgorithm
{
    private static readonly Dictionary<string, int> PriorityOrder = new Dictionary<string, int>
    {
        { "urgent", 0 },
        { "high", 1 },
        { "medium", 2 },
        { "low", 3 }
    };

    public static TodosReviewResult Run(TodosContext ctx)
    {
        var active = ctx.todos
            .Where(t => t.status == "pending" || t.status == "in_progress")
            .ToList();
        
        if (!string.IsNullOrEmpty(ctx.filterContext))
            active = active.Where(t => t.context == ctx.filterContext).ToList();
        
        var urgent = active.Where(t => t.priority == "urgent").ToList();
        var overdue = active.Where(t => t.dueDate.HasValue && t.dueDate.Value.Date < ctx.currentDate.Date).ToList();
        var today = active.Where(t => t.dueDate.HasValue && t.dueDate.Value.Date == ctx.currentDate.Date).ToList();
        
        var nextActions = active
            .OrderBy(t => PriorityOrder.GetValueOrDefault(t.priority, 99))
            .ThenBy(t => t.createdDate)
            .Take(ctx.maxDisplay)
            .ToList();
        
        var notes = new List<string>();
        if (urgent.Count > 0)
            notes.Add($"🔴 {urgent.Count} URGENT item(s)!");
        if (overdue.Count > 0)
            notes.Add($"⚠️ {overdue.Count} overdue item(s).");
        if (today.Count > 0)
            notes.Add($"📅 {today.Count} item(s) due today.");
        notes.Add($"📋 {active.Count} total active items.");
        
        return new TodosReviewResult
        {
            urgent = urgent,
            today = today,
            overdue = overdue,
            nextActions = nextActions,
            note = string.Join(" ", notes)
        };
    }
}
