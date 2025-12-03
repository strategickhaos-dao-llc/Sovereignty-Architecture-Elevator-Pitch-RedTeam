// cpp/src/reviews.h
#pragma once
#include <string>
#include <vector>
#include <chrono>
#include <ctime>

// ============ Homework Review ============

struct HomeworkItem {
    std::string id;
    std::string title;
    std::string subject;
    std::tm due_date;
    std::string status; // "not_started", "in_progress", "completed"
    int priority;       // 1 = highest
};

struct HomeworkContext {
    std::vector<HomeworkItem> items;
    std::tm current_date;
    int max_priorities = 3;
};

struct HomeworkReviewResult {
    std::vector<HomeworkItem> overdue;
    std::vector<HomeworkItem> due_today;
    std::vector<HomeworkItem> upcoming;
    std::vector<HomeworkItem> top_priorities;
    std::string note;
};

class ReviewHomeworkTask {
public:
    HomeworkReviewResult run(const HomeworkContext& ctx);
private:
    bool date_less_than(const std::tm& a, const std::tm& b);
    bool date_equal(const std::tm& a, const std::tm& b);
};

// ============ Bills Review ============

struct BillItem {
    std::string id;
    std::string name;
    double amount;
    std::tm due_date;
    std::string category;
    bool is_paid;
    bool is_autopay;
};

struct BillsContext {
    std::vector<BillItem> bills;
    std::tm current_date;
    int warning_days = 7;
};

struct BillsReviewResult {
    std::vector<BillItem> overdue;
    std::vector<BillItem> due_soon;
    std::vector<BillItem> upcoming;
    double total_due_soon;
    std::string note;
};

class ReviewBillsTask {
public:
    BillsReviewResult run(const BillsContext& ctx);
private:
    bool date_less_than(const std::tm& a, const std::tm& b);
    bool date_less_equal(const std::tm& a, const std::tm& b);
    std::tm add_days(const std::tm& date, int days);
};

// ============ Todos Review ============

struct TodoItem {
    std::string id;
    std::string title;
    bool has_due_date;
    std::tm due_date;
    std::tm created_date;
    std::string status;   // "pending", "in_progress", "completed", "cancelled"
    std::string priority; // "low", "medium", "high", "urgent"
    std::string context;  // "home", "work", "errands", "personal"
};

struct TodosContext {
    std::vector<TodoItem> todos;
    std::tm current_date;
    std::string filter_context;
    int max_display = 5;
};

struct TodosReviewResult {
    std::vector<TodoItem> urgent;
    std::vector<TodoItem> today;
    std::vector<TodoItem> overdue;
    std::vector<TodoItem> next_actions;
    std::string note;
};

class ReviewTodosTask {
public:
    TodosReviewResult run(const TodosContext& ctx);
private:
    int priority_order(const std::string& priority);
    bool date_less_than(const std::tm& a, const std::tm& b);
    bool date_equal(const std::tm& a, const std::tm& b);
};
