# Commence Evolution Time (CET) - Module Completion System

**A focused homework/coursework management ritual where you and all nodes work together on academic assignments.**

---

## 🎯 What Is Commence Evolution Time?

**CET (Commence Evolution Time)** is a dedicated 60–90 minute block where:

- 🧠 **You** = focus exclusively on homework/coursework
- 🖥️ **All nodes** (Strategickhaos AI, Jarvis, Lyra, Nova, Athena) = support academic work, not side projects

Think of it as a **department meeting** where everyone shows up, but the agenda is **SNHU modules only** (or whatever coursework you're working on).

---

## 🚀 The 5-Minute Ritual to Start Each Session

When you say: **"Commence Evolution: Homework Mode"**

### Do This:

#### 1. **Open Only 3 Things**
   - Your **LMS / course dashboard**
   - A **single notes doc** (Obsidian, Notepad, or use `templates/homework_tracker.md`)
   - This chat (your AI assistant 💅)

#### 2. **Brain Dump Homework**
   
   Copy the homework tracker template:
   ```bash
   cp templates/homework_tracker.md ~/current_homework_tracker.md
   ```
   
   Or create your own table:
   ```text
   COURSE  | MODULE / ASSIGNMENT       | DUE DATE | EST. TIME | STATUS
   ------- | ------------------------- | -------- | --------- | ------
   IT-140  | Module X – [name]         |          |           | 
   MATH    | Module X – [name]         |          |           | 
   OTHER   | ...                       |          |           | 
   ```

   Don't overthink. Just list everything that's on your mind.

#### 3. **Pick ONE "Boss Assignment" for This Block**

   - Not all of them.
   - Choose either:
     - **Earliest due** OR
     - **Biggest grade impact**

   Put a ⭐ star next to it. That's tonight's boss.

---

## ⏱️ The CE-75 Session Template (75 minutes)

Here's the default **75-minute block** structure:

### 🔁 Cycle 1 (30 minutes total)

**25 min – Deep Work on Boss Assignment**
- No new tabs
- Just: read prompt → outline → start

**5 min – Log Progress**
- Write 2–3 bullets in your notes:
  ```text
  CE-75 / Cycle 1:
  - Read full instructions for [assignment].
  - Created outline.
  - Started section 1.
  ```

### 🔁 Cycle 2 (30 minutes total)

**25 min – Continue / Implement**
- If coding: write the actual code
- If writing: fill out sections

**5 min – Mini Sync**
- Note where you stopped and what's next:
  ```text
  CE-75 / Cycle 2:
  - Completed sections A & B.
  - Next: test / proofread / final polish.
  ```

### 🔁 Cycle 3 (15 minutes total)

**10 min – Polish / Submit or Get to "90%"**
- If it's close, submit
- If not, leave a clear "Next Steps" marker

**5 min – Closeout**
- Update your table's STATUS column:
  - "✅ Submitted"
  - "🟡 80% done – needs final check"
  - "🟥 Not started"

---

## ⚡ The CE-45 (45-minute Express Session)

For when you're tired but need to maintain momentum:

- **25 min – Deep Work** (one focused task)
- **5 min – Log Progress**
- **15 min – Push Forward** (make it submittable or clearly define next steps)

---

## 🤖 How the Nodes Attend This Department Meeting

Each node has a specific role during CET:

### **Lyra (Right-brain / Creative)**
- **Job**: Formatting, variable names, commenting code, making things readable
- **When to call**: When you're stuck making something *clearer*, not for new wild ideas

### **Nova (Left-brain / Logic)**
- **Job**: Algorithms, math, debugging
- **When to call**: When stuck, write the problem in plain English, then let "Nova" mode think:
  - "What is this really asking?"
  - "What are the inputs and outputs?"

### **Athena / Strategickhaos Core**
- **Job**: Keep the **big picture**
- **End of session**: Athena writes a 2–3 sentence summary:
  ```text
  Today's Evolution Log:
  - Finished X.
  - Advanced Y.
  - Tomorrow's target: Z.
  ```

### **Me (GPT / Baby Mama)**
- **Job**: Turn assignments into bite-sized steps, pseudo-code, or starter code
- **How to use**: Drop the homework prompt and say:
  > "Break this into CE-75 steps and give me the first one."

---

## 📅 Daily Minimum: One CE Block

**Non-negotiable minimum:**

> 🎯 **One CE-75 block per day**  
> (If exhausted, do a **CE-45** = 25 min work + 5 min log + 15 min push)

That's it. No guilt beyond that.

Track your streak using the evolution log template:
```bash
cp templates/evolution_log.md ~/my_evolution_log.md
```

Or manually:
```text
Commence Evolution Log

[ ] Day 1 – CE-75 done?
[ ] Day 2 – CE-75 done?
[ ] Day 3 – CE-75 done?
...
```

We care about **streaks**, not perfection.

---

## 🛠️ Quick Start Scripts

### First Time Setup
Make the scripts executable (one-time setup):
```bash
chmod +x scripts/start-ce-session.sh scripts/ce-log-progress.sh
```

### Start a New CE Session
```bash
./scripts/start-ce-session.sh
```

This will:
1. Create a dated session file
2. Copy the homework tracker template
3. Start a timer
4. Open your notes

### Log Progress During a Cycle
```bash
./scripts/ce-log-progress.sh "Completed sections A & B. Next: testing."
```

---

## 💼 Advanced: AI-Driven Planning

If you paste **your current module list** (even messy, straight from SNHU), your AI assistant can:

- Turn it into a **priority table**
- Plan out **the next 3–5 CE-75 sessions** in order
- Write exact micro-steps like:
  - "Open zyBooks → go to Section 4.3 → complete activities 1–5"

### How to Use:
```text
Paste your assignments here and say:
"Here's my course load. Create a 5-session CE-75 plan prioritized by due date."
```

---

## 🎬 Tonight's Action

1. **Open your course dashboard**
2. **Start a CE-75**
3. **Drop your Boss Assignment** in chat and say:
   > "Here's the prompt, run CE-75 Cycle 1 for me."

And we'll sit in the **Department of Module Completion** together until it's done. 💻🧠💙

---

## 📁 Related Resources

- **[Session Template](templates/ce_session_template.md)** - Pre-formatted session structure
- **[Homework Tracker](templates/homework_tracker.md)** - Assignment tracking table
- **[Evolution Log](templates/evolution_log.md)** - Daily progress tracking
- **[Node Roles](governance/node_roles_cet.yaml)** - Detailed node responsibilities during CET
- **[CE-75 Example](examples/ce75_example.md)** - Full walkthrough of a 75-minute session
- **[CE-45 Example](examples/ce45_example.md)** - Express 45-minute session example

---

**Built with 🔥 for Future You**

*"The babies are fancy, but school pays the bills. Let's do this together."* 💪
