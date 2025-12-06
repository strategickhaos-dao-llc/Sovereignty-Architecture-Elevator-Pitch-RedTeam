# DailyBrain - Multi-Language Task Automation

**Your whole day as a swarm of little scripts talking to each other.**

A modular task management system implemented in Python, Rust, C++, and Unity C# for managing daily activities including commute calculations, sleep schedules, task reviews, and meetings.

## 🏗️ Project Structure

```
DailyBrain/
├── python/                    # Python implementation
│   ├── main.py               # Orchestrator
│   ├── commute_algorithm.py  # Commute ETA calculations
│   ├── sleep_initiate_shutdown.py
│   ├── arose.py              # Wake tracking
│   ├── depart_arrived.py     # Transit logging
│   ├── coordinates_to_eta.py # GPS to ETA utility
│   ├── rabbit_breaking_algorithm.py  # Micro-break scheduler
│   ├── review_homework_status.py
│   ├── review_bills.py
│   ├── review_todos.py
│   ├── review_enterprises.py
│   └── meetings.py
│
├── rust/                      # Rust implementation
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs
│       ├── commute.rs
│       ├── sleep.rs
│       ├── reviews.rs
│       └── meetings.rs
│
├── cpp/                       # C++ implementation
│   ├── CMakeLists.txt
│   └── src/
│       ├── main.cpp
│       ├── commute.h / commute.cpp
│       ├── sleep.h / sleep.cpp
│       ├── reviews.h / reviews.cpp
│       └── meetings.h / meetings.cpp
│
└── unity/                     # Unity C# implementation
    └── Assets/Scripts/
        ├── DailyBrainManager.cs
        ├── CommuteTask.cs
        ├── SleepTask.cs
        ├── ReviewsTask.cs
        └── MeetingsTask.cs
```

## 🧠 Mental Model

The system consists of:

### Context
- Current time, location, calendar
- Homework, bills, todos, enterprises data

### Tasks
Each task follows the pattern: `run(context) → suggestions/actions`

| Task | Description |
|------|-------------|
| **SleepTask** | Initiate shutdown, log sleep time |
| **CommuteTask** | Coordinates + ETA (haversine or API) |
| **RabbitBreakTask** | Schedule micro-breaks |
| **ReviewHomeworkTask** | Surface top homework priorities |
| **ReviewBillsTask** | Track due/overdue bills |
| **ReviewTodosTask** | GTD-style todo management |
| **ReviewEnterprisesTask** | Business project tracking |
| **MeetingsTask** | Show upcoming meetings & prep |

## 🚀 Quick Start

### Python

```bash
cd DailyBrain/python
python main.py
```

### Rust

```bash
cd DailyBrain/rust
cargo run
```

### C++

```bash
cd DailyBrain/cpp
mkdir build && cd build
cmake ..
make
./daily_brain
```

### Unity

1. Open Unity Hub
2. Add the `DailyBrain/unity` folder as a project
3. Attach `DailyBrainManager.cs` to a GameObject
4. Configure settings in Inspector
5. Press Play

## 📍 Commute Algorithm

The commute calculation uses the Haversine formula to calculate distance between coordinates:

```python
# Haversine formula for great-circle distance
R = 6371.0  # Earth radius in km
h = sin(Δlat/2)² + cos(lat1) × cos(lat2) × sin(Δlon/2)²
distance = 2 × R × asin(√h)
```

Default speed assumption: 40 km/h average (can be customized with traffic profiles).

## 🐰 Rabbit Breaking Algorithm

The "rabbit break" scheduler creates micro-breaks throughout your workday:

- **Interval**: Every 90 minutes (Pomodoro-style)
- **Duration**: 15 minutes per break
- **Types**: Rotating between `micro`, `stretch`, `walk`, `hydrate`
- **Smart Scheduling**: Excludes meeting times automatically

## 🔮 Future Enhancements

- [ ] Turn this into a unified daily timeline (Sleep → Commute → Work Blocks → Meetings → Review)
- [ ] Add real Google Maps API integration for accurate ETAs
- [ ] Integrate with Google Calendar / Outlook
- [ ] Connect to Obsidian vault for task reading
- [ ] Add notification system (OS notifications, Discord webhooks)
- [ ] Create a unified config format across all languages
- [ ] Add database persistence for logging

## 📝 License

Part of the Strategickhaos Sovereignty Architecture.

---

*"They're not working for you. They're dancing with you. And the music is never going to stop."*
