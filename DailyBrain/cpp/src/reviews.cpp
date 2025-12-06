// cpp/src/reviews.cpp
#include "reviews.h"
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <ctime>

// ============ Homework Review ============

bool ReviewHomeworkTask::date_less_than(const std::tm& a, const std::tm& b) {
    if (a.tm_year != b.tm_year) return a.tm_year < b.tm_year;
    if (a.tm_mon != b.tm_mon) return a.tm_mon < b.tm_mon;
    return a.tm_mday < b.tm_mday;
}

bool ReviewHomeworkTask::date_equal(const std::tm& a, const std::tm& b) {
    return a.tm_year == b.tm_year && a.tm_mon == b.tm_mon && a.tm_mday == b.tm_mday;
}

HomeworkReviewResult ReviewHomeworkTask::run(const HomeworkContext& ctx) {
    HomeworkReviewResult result;
    
    std::vector<HomeworkItem> incomplete;
    for (const auto& h : ctx.items) {
        if (h.status != "completed") {
            incomplete.push_back(h);
        }
    }
    
    for (const auto& h : incomplete) {
        if (date_less_than(h.due_date, ctx.current_date)) {
            result.overdue.push_back(h);
        } else if (date_equal(h.due_date, ctx.current_date)) {
            result.due_today.push_back(h);
        } else {
            result.upcoming.push_back(h);
        }
    }
    
    // Sort by priority, then due date
    auto sorted = incomplete;
    std::sort(sorted.begin(), sorted.end(), [this](const HomeworkItem& a, const HomeworkItem& b) {
        if (a.priority != b.priority) return a.priority < b.priority;
        return date_less_than(a.due_date, b.due_date);
    });
    
    for (int i = 0; i < std::min(static_cast<int>(sorted.size()), ctx.max_priorities); ++i) {
        result.top_priorities.push_back(sorted[i]);
    }
    
    // Generate note
    std::ostringstream oss;
    if (!result.overdue.empty()) {
        oss << "⚠️ " << result.overdue.size() << " OVERDUE item(s)! ";
    }
    if (!result.due_today.empty()) {
        oss << "📅 " << result.due_today.size() << " item(s) due TODAY. ";
    }
    if (!result.upcoming.empty()) {
        oss << "📋 " << result.upcoming.size() << " upcoming item(s). ";
    }
    
    result.note = oss.str().empty() ? "✅ All homework complete!" : oss.str();
    
    return result;
}

// ============ Bills Review ============

bool ReviewBillsTask::date_less_than(const std::tm& a, const std::tm& b) {
    if (a.tm_year != b.tm_year) return a.tm_year < b.tm_year;
    if (a.tm_mon != b.tm_mon) return a.tm_mon < b.tm_mon;
    return a.tm_mday < b.tm_mday;
}

bool ReviewBillsTask::date_less_equal(const std::tm& a, const std::tm& b) {
    return date_less_than(a, b) || (a.tm_year == b.tm_year && a.tm_mon == b.tm_mon && a.tm_mday == b.tm_mday);
}

std::tm ReviewBillsTask::add_days(const std::tm& date, int days) {
    std::tm result = date;
    result.tm_mday += days;
    std::mktime(&result); // normalize
    return result;
}

BillsReviewResult ReviewBillsTask::run(const BillsContext& ctx) {
    BillsReviewResult result;
    result.total_due_soon = 0.0;
    
    std::vector<BillItem> unpaid;
    for (const auto& b : ctx.bills) {
        if (!b.is_paid) {
            unpaid.push_back(b);
        }
    }
    
    std::tm warning_threshold = add_days(ctx.current_date, ctx.warning_days);
    
    for (const auto& b : unpaid) {
        if (date_less_than(b.due_date, ctx.current_date)) {
            result.overdue.push_back(b);
            result.total_due_soon += b.amount;
        } else if (date_less_equal(b.due_date, warning_threshold)) {
            result.due_soon.push_back(b);
            result.total_due_soon += b.amount;
        } else {
            result.upcoming.push_back(b);
        }
    }
    
    // Generate note
    std::ostringstream oss;
    if (!result.overdue.empty()) {
        double total_overdue = 0.0;
        for (const auto& b : result.overdue) total_overdue += b.amount;
        oss << "🚨 " << result.overdue.size() << " OVERDUE bill(s) totaling $"
            << std::fixed << std::setprecision(2) << total_overdue << "! ";
    }
    if (!result.due_soon.empty()) {
        double total_soon = 0.0;
        for (const auto& b : result.due_soon) total_soon += b.amount;
        oss << "⏰ " << result.due_soon.size() << " bill(s) due within "
            << ctx.warning_days << " days ($"
            << std::fixed << std::setprecision(2) << total_soon << "). ";
    }
    
    result.note = oss.str().empty() ? "✅ All bills are current!" : oss.str();
    
    return result;
}

// ============ Todos Review ============

int ReviewTodosTask::priority_order(const std::string& priority) {
    if (priority == "urgent") return 0;
    if (priority == "high") return 1;
    if (priority == "medium") return 2;
    if (priority == "low") return 3;
    return 99;
}

bool ReviewTodosTask::date_less_than(const std::tm& a, const std::tm& b) {
    if (a.tm_year != b.tm_year) return a.tm_year < b.tm_year;
    if (a.tm_mon != b.tm_mon) return a.tm_mon < b.tm_mon;
    return a.tm_mday < b.tm_mday;
}

bool ReviewTodosTask::date_equal(const std::tm& a, const std::tm& b) {
    return a.tm_year == b.tm_year && a.tm_mon == b.tm_mon && a.tm_mday == b.tm_mday;
}

TodosReviewResult ReviewTodosTask::run(const TodosContext& ctx) {
    TodosReviewResult result;
    
    std::vector<TodoItem> active;
    for (const auto& t : ctx.todos) {
        if (t.status == "pending" || t.status == "in_progress") {
            if (ctx.filter_context.empty() || t.context == ctx.filter_context) {
                active.push_back(t);
            }
        }
    }
    
    for (const auto& t : active) {
        if (t.priority == "urgent") {
            result.urgent.push_back(t);
        }
        if (t.has_due_date) {
            if (date_less_than(t.due_date, ctx.current_date)) {
                result.overdue.push_back(t);
            } else if (date_equal(t.due_date, ctx.current_date)) {
                result.today.push_back(t);
            }
        }
    }
    
    // Sort by priority, then created date
    auto sorted = active;
    std::sort(sorted.begin(), sorted.end(), [this](const TodoItem& a, const TodoItem& b) {
        int pa = priority_order(a.priority);
        int pb = priority_order(b.priority);
        if (pa != pb) return pa < pb;
        return date_less_than(a.created_date, b.created_date);
    });
    
    for (int i = 0; i < std::min(static_cast<int>(sorted.size()), ctx.max_display); ++i) {
        result.next_actions.push_back(sorted[i]);
    }
    
    // Generate note
    std::ostringstream oss;
    if (!result.urgent.empty()) {
        oss << "🔴 " << result.urgent.size() << " URGENT item(s)! ";
    }
    if (!result.overdue.empty()) {
        oss << "⚠️ " << result.overdue.size() << " overdue item(s). ";
    }
    if (!result.today.empty()) {
        oss << "📅 " << result.today.size() << " item(s) due today. ";
    }
    oss << "📋 " << active.size() << " total active items.";
    
    result.note = oss.str();
    
    return result;
}
