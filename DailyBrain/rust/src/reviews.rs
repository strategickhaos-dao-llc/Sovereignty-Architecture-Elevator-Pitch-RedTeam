// rust/src/reviews.rs
use chrono::NaiveDate;

// ============ Homework Review ============

#[derive(Clone, Debug)]
pub struct HomeworkItem {
    pub id: String,
    pub title: String,
    pub subject: String,
    pub due_date: NaiveDate,
    pub status: String, // "not_started", "in_progress", "completed"
    pub priority: i32,  // 1 = highest
}

pub struct HomeworkContext {
    pub items: Vec<HomeworkItem>,
    pub current_date: NaiveDate,
    pub max_priorities: usize,
}

pub struct HomeworkReviewResult {
    pub overdue: Vec<HomeworkItem>,
    pub due_today: Vec<HomeworkItem>,
    pub upcoming: Vec<HomeworkItem>,
    pub top_priorities: Vec<HomeworkItem>,
    pub note: String,
}

pub struct ReviewHomeworkTask;

impl ReviewHomeworkTask {
    pub fn run(&self, ctx: &HomeworkContext) -> HomeworkReviewResult {
        let incomplete: Vec<_> = ctx
            .items
            .iter()
            .filter(|h| h.status != "completed")
            .cloned()
            .collect();

        let overdue: Vec<_> = incomplete
            .iter()
            .filter(|h| h.due_date < ctx.current_date)
            .cloned()
            .collect();

        let due_today: Vec<_> = incomplete
            .iter()
            .filter(|h| h.due_date == ctx.current_date)
            .cloned()
            .collect();

        let upcoming: Vec<_> = incomplete
            .iter()
            .filter(|h| h.due_date > ctx.current_date)
            .cloned()
            .collect();

        let mut sorted = incomplete.clone();
        sorted.sort_by(|a, b| {
            a.priority
                .cmp(&b.priority)
                .then_with(|| a.due_date.cmp(&b.due_date))
        });
        let top_priorities: Vec<_> = sorted.into_iter().take(ctx.max_priorities).collect();

        let mut notes = Vec::new();
        if !overdue.is_empty() {
            notes.push(format!("⚠️ {} OVERDUE item(s)!", overdue.len()));
        }
        if !due_today.is_empty() {
            notes.push(format!("📅 {} item(s) due TODAY.", due_today.len()));
        }
        if !upcoming.is_empty() {
            notes.push(format!("📋 {} upcoming item(s).", upcoming.len()));
        }

        let note = if notes.is_empty() {
            "✅ All homework complete!".to_string()
        } else {
            notes.join(" ")
        };

        HomeworkReviewResult {
            overdue,
            due_today,
            upcoming,
            top_priorities,
            note,
        }
    }
}

// ============ Bills Review ============

#[derive(Clone, Debug)]
pub struct BillItem {
    pub id: String,
    pub name: String,
    pub amount: f64,
    pub due_date: NaiveDate,
    pub category: String,
    pub is_paid: bool,
    pub is_autopay: bool,
}

pub struct BillsContext {
    pub bills: Vec<BillItem>,
    pub current_date: NaiveDate,
    pub warning_days: i64,
}

pub struct BillsReviewResult {
    pub overdue: Vec<BillItem>,
    pub due_soon: Vec<BillItem>,
    pub upcoming: Vec<BillItem>,
    pub total_due_soon: f64,
    pub note: String,
}

pub struct ReviewBillsTask;

impl ReviewBillsTask {
    pub fn run(&self, ctx: &BillsContext) -> BillsReviewResult {
        let unpaid: Vec<_> = ctx.bills.iter().filter(|b| !b.is_paid).cloned().collect();

        let overdue: Vec<_> = unpaid
            .iter()
            .filter(|b| b.due_date < ctx.current_date)
            .cloned()
            .collect();

        let warning_threshold = ctx.current_date + chrono::Duration::days(ctx.warning_days);
        let due_soon: Vec<_> = unpaid
            .iter()
            .filter(|b| b.due_date >= ctx.current_date && b.due_date <= warning_threshold)
            .cloned()
            .collect();

        let upcoming: Vec<_> = unpaid
            .iter()
            .filter(|b| b.due_date > warning_threshold)
            .cloned()
            .collect();

        let total_due_soon: f64 = overdue.iter().chain(due_soon.iter()).map(|b| b.amount).sum();

        let mut notes = Vec::new();
        if !overdue.is_empty() {
            let total_overdue: f64 = overdue.iter().map(|b| b.amount).sum();
            notes.push(format!(
                "🚨 {} OVERDUE bill(s) totaling ${:.2}!",
                overdue.len(),
                total_overdue
            ));
        }
        if !due_soon.is_empty() {
            let total_soon: f64 = due_soon.iter().map(|b| b.amount).sum();
            notes.push(format!(
                "⏰ {} bill(s) due within {} days (${:.2}).",
                due_soon.len(),
                ctx.warning_days,
                total_soon
            ));
        }

        let note = if notes.is_empty() {
            "✅ All bills are current!".to_string()
        } else {
            notes.join(" ")
        };

        BillsReviewResult {
            overdue,
            due_soon,
            upcoming,
            total_due_soon,
            note,
        }
    }
}

// ============ Todos Review ============

#[derive(Clone, Debug)]
pub struct TodoItem {
    pub id: String,
    pub title: String,
    pub due_date: Option<NaiveDate>,
    pub created_date: NaiveDate,
    pub status: String,   // "pending", "in_progress", "completed", "cancelled"
    pub priority: String, // "low", "medium", "high", "urgent"
    pub context: String,  // "home", "work", "errands", "personal"
}

pub struct TodosContext {
    pub todos: Vec<TodoItem>,
    pub current_date: NaiveDate,
    pub filter_context: Option<String>,
    pub max_display: usize,
}

pub struct TodosReviewResult {
    pub urgent: Vec<TodoItem>,
    pub today: Vec<TodoItem>,
    pub overdue: Vec<TodoItem>,
    pub next_actions: Vec<TodoItem>,
    pub note: String,
}

pub struct ReviewTodosTask;

impl ReviewTodosTask {
    fn priority_order(priority: &str) -> i32 {
        match priority {
            "urgent" => 0,
            "high" => 1,
            "medium" => 2,
            "low" => 3,
            _ => 99,
        }
    }

    pub fn run(&self, ctx: &TodosContext) -> TodosReviewResult {
        let mut active: Vec<_> = ctx
            .todos
            .iter()
            .filter(|t| t.status == "pending" || t.status == "in_progress")
            .cloned()
            .collect();

        if let Some(ref filter) = ctx.filter_context {
            active.retain(|t| &t.context == filter);
        }

        let urgent: Vec<_> = active
            .iter()
            .filter(|t| t.priority == "urgent")
            .cloned()
            .collect();

        let overdue: Vec<_> = active
            .iter()
            .filter(|t| t.due_date.map_or(false, |d| d < ctx.current_date))
            .cloned()
            .collect();

        let today: Vec<_> = active
            .iter()
            .filter(|t| t.due_date == Some(ctx.current_date))
            .cloned()
            .collect();

        let mut sorted = active.clone();
        sorted.sort_by(|a, b| {
            Self::priority_order(&a.priority)
                .cmp(&Self::priority_order(&b.priority))
                .then_with(|| a.created_date.cmp(&b.created_date))
        });
        let next_actions: Vec<_> = sorted.into_iter().take(ctx.max_display).collect();

        let mut notes = Vec::new();
        if !urgent.is_empty() {
            notes.push(format!("🔴 {} URGENT item(s)!", urgent.len()));
        }
        if !overdue.is_empty() {
            notes.push(format!("⚠️ {} overdue item(s).", overdue.len()));
        }
        if !today.is_empty() {
            notes.push(format!("📅 {} item(s) due today.", today.len()));
        }
        notes.push(format!("📋 {} total active items.", active.len()));

        TodosReviewResult {
            urgent,
            today,
            overdue,
            next_actions,
            note: notes.join(" "),
        }
    }
}
