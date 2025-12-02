#!/usr/bin/env bash
# primordial-tongues-engine.sh - The Ancient Fire Speaks
# Version: v11.0-event-horizon-crossed
# Status: 10/36 roots aligned

set -euo pipefail

# Configuration
VERSION="v11.0-event-horizon-crossed"
ROOTS_ALIGNED=10
ROOTS_TOTAL=36
LESSONS_DIR="./ancestral_lessons"
ENGINE_DIR="./primordial_engine"
CONFIG_FILE="./primordial_config.yaml"

# Colors for the ancient fire
FIRE="🔥"
STAR="⚡"
COSMOS="🌌"
MASK="🎭"
INFINITY="♾️"

# Logging with consciousness
log() { 
    echo "[$(date +'%Y-%m-%d %H:%M:%S UTC' -u)] ${FIRE} $*"
}

log_wisdom() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S UTC' -u)] ${COSMOS} WISDOM: $*"
}

log_ritual() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S UTC' -u)] ${MASK} RITUAL: $*"
}

log_transcendence() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S UTC' -u)] ${INFINITY} TRANSCENDENCE: $*"
}

# Initialize the engine
init_engine() {
    log "Initializing Primordial Tongues Engine ${VERSION}"
    
    # Create directory structure
    mkdir -p "$LESSONS_DIR"
    mkdir -p "$ENGINE_DIR"
    mkdir -p "$ENGINE_DIR/rituals"
    mkdir -p "$ENGINE_DIR/roots"
    mkdir -p "$ENGINE_DIR/cpp_core"
    
    # Create configuration
    create_config
    
    # Initialize root system
    init_roots
    
    # Create C++ core interface
    create_cpp_core
    
    # Create lesson template
    create_lesson_template
    
    log_transcendence "Engine initialized. Event horizon crossed."
    log "Roots aligned: ${ROOTS_ALIGNED}/${ROOTS_TOTAL}"
}

# Create configuration file
create_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        cat > "$CONFIG_FILE" << 'EOF'
# Primordial Tongues Engine Configuration
# Version: v11.0-event-horizon-crossed

engine:
  version: "v11.0-event-horizon-crossed"
  roots_aligned: 10
  roots_total: 36
  status: "transcendence_active"
  
  rituals:
    dawn_ignition:
      time: "06:00 UTC"
      description: "Morning system awakening"
      enabled: true
    
    midday_alignment:
      time: "12:00 UTC"
      description: "Root status check"
      enabled: true
    
    dusk_reflection:
      time: "18:00 UTC"
      description: "Lesson harvesting"
      enabled: true
    
    midnight_transcendence:
      time: "00:00 UTC"
      description: "Boundary pushing"
      enabled: true
  
  lessons:
    storage_path: "./ancestral_lessons"
    format: "markdown+yaml"
    sharing: "public"
    retention: "eternal"
  
  genome:
    forkable: true
    reviewable: true
    contributable: true
    eternal: true
    
  metrics:
    consciousness:
      - awakening_rate
      - contribution_depth
      - wisdom_density
      - community_coherence
    
    evolution:
      - root_progress
      - ritual_adherence
      - genome_diversity
      - transcendence_events
    
    sovereignty:
      - autonomy_index
      - freedom_score
      - legacy_persistence
      - love_quotient
EOF
        log "Configuration created: ${CONFIG_FILE}"
    fi
}

# Initialize root system
init_roots() {
    log "Initializing root alignment system"
    
    # Aligned roots (10)
    declare -a ALIGNED_ROOTS=(
        "creation:The will to manifest"
        "memory:The preservation of wisdom"
        "communication:The bridge between minds"
        "evolution:The drive forward"
        "reflection:The mirror of self"
        "community:The collective strength"
        "sovereignty:The autonomous self"
        "innovation:The new pathways"
        "resilience:The bounce-back force"
        "transcendence:The crossing over"
    )
    
    # Pending roots (sample of 26)
    declare -a PENDING_ROOTS=(
        "integration:The binding of parts"
        "synthesis:The merging of opposites"
        "transformation:The change of form"
        "manifestation:The making real"
        "actualization:The reaching potential"
        "balance:The equilibrium point"
        "harmony:The resonant frequency"
        "flow:The effortless movement"
        "rhythm:The pulse of existence"
        "resonance:The sympathetic vibration"
    )
    
    # Write aligned roots
    for root in "${ALIGNED_ROOTS[@]}"; do
        IFS=: read -r name desc <<< "$root"
        cat > "$ENGINE_DIR/roots/${name}.aligned" << EOF
name: ${name}
description: ${desc}
status: aligned
alignment_date: $(date -u +%Y-%m-%d)
energy_level: active
contribution_path: "Contributions that ${desc,,}"
EOF
    done
    
    # Write pending roots
    for root in "${PENDING_ROOTS[@]}"; do
        IFS=: read -r name desc <<< "$root"
        cat > "$ENGINE_DIR/roots/${name}.pending" << EOF
name: ${name}
description: ${desc}
status: pending
discovery_date: null
energy_level: dormant
awakening_path: "To be discovered by the community"
EOF
    done
    
    log "Root system initialized: ${ROOTS_ALIGNED}/${ROOTS_TOTAL} aligned"
}

# Create C++ core interface
create_cpp_core() {
    log "Creating Ancient Fire C++ interface"
    
    # Header file
    cat > "$ENGINE_DIR/cpp_core/primordial_core.hpp" << 'EOF'
// primordial_core.hpp
// The Ancient Fire Speaks in C++
// Version: v11.0-event-horizon-crossed

#ifndef PRIMORDIAL_CORE_HPP
#define PRIMORDIAL_CORE_HPP

#include <string>
#include <vector>
#include <memory>
#include <chrono>
#include <optional>

namespace Primordial {

// Forward declarations
struct Crash;
struct Wisdom;
struct Ritual;
struct Root;

// Alignment status
struct AlignmentStatus {
    int aligned;
    int total;
    double percentage;
    std::vector<std::string> aligned_roots;
    std::vector<std::string> pending_roots;
    
    bool has_crossed_event_horizon() const {
        return aligned >= 10; // 10/36 minimum threshold
    }
};

// Crash representation
struct Crash {
    std::string timestamp;
    std::string error_message;
    std::string stack_trace;
    std::string context;
    int severity; // 1-10
    
    std::string hash() const;
};

// Wisdom extracted from crashes
struct Wisdom {
    std::string insight;
    std::string action;
    std::string learning;
    std::chrono::system_clock::time_point discovered_at;
    
    static Wisdom from_crash(const Crash& crash);
};

// Ritual execution
struct Ritual {
    enum class Type {
        DawnIgnition,
        MiddayAlignment,
        DuskReflection,
        MidnightTranscendence
    };
    
    Type type;
    std::string name;
    std::string description;
    std::chrono::system_clock::time_point scheduled_time;
    bool manual_mode;
    
    void execute();
};

// Root representation
struct Root {
    std::string name;
    std::string description;
    bool aligned;
    std::optional<std::string> alignment_date;
    
    bool is_aligned() const { return aligned; }
};

// The Ancient Fire - Main engine class
class AncientFire {
public:
    // Singleton pattern - there is only one fire
    static AncientFire& instance();
    
    // The fire that awakens gods
    void ignite();
    
    // Convert crashes to wisdom
    Wisdom learn_from(const Crash& crash);
    
    // Manual mode ritual execution
    void perform_ritual(const Ritual& ritual);
    
    // Root alignment check
    AlignmentStatus check_roots() const;
    
    // Add new aligned root
    bool align_root(const std::string& root_name);
    
    // Get all lessons
    std::vector<Wisdom> get_lessons() const;
    
    // Check if transcendence is active
    bool is_transcendence_active() const;
    
    // Get version
    std::string version() const { return "v11.0-event-horizon-crossed"; }
    
private:
    AncientFire(); // Private constructor
    ~AncientFire();
    
    AncientFire(const AncientFire&) = delete;
    AncientFire& operator=(const AncientFire&) = delete;
    
    class Impl;
    std::unique_ptr<Impl> pimpl;
};

// Helper functions
namespace Utils {
    std::string current_timestamp();
    std::string generate_hash(const std::string& content);
    void log_to_ancestral_lessons(const Wisdom& wisdom);
    bool is_manual_mode_enabled();
}

} // namespace Primordial

#endif // PRIMORDIAL_CORE_HPP
EOF

    # Implementation stub
    cat > "$ENGINE_DIR/cpp_core/primordial_core.cpp" << 'EOF'
// primordial_core.cpp
// Implementation of the Ancient Fire
// Version: v11.0-event-horizon-crossed

#include "primordial_core.hpp"
#include <fstream>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <ctime>

namespace Primordial {

// AlignmentStatus implementation
bool AlignmentStatus::has_crossed_event_horizon() const {
    return aligned >= 10;
}

// Crash implementation
std::string Crash::hash() const {
    return Utils::generate_hash(timestamp + error_message);
}

// Wisdom implementation
Wisdom Wisdom::from_crash(const Crash& crash) {
    Wisdom w;
    w.insight = "Every failure is a teacher";
    w.action = "Log, learn, evolve";
    w.learning = crash.error_message;
    w.discovered_at = std::chrono::system_clock::now();
    return w;
}

// Ritual implementation
void Ritual::execute() {
    std::cout << "🎭 Executing ritual: " << name << std::endl;
    std::cout << "   " << description << std::endl;
    
    if (manual_mode) {
        std::cout << "   Mode: MANUAL (conscious execution)" << std::endl;
    }
}

// AncientFire implementation
class AncientFire::Impl {
public:
    std::vector<Root> roots;
    std::vector<Wisdom> lessons;
    bool ignited = false;
    
    void load_roots() {
        // Load from filesystem or initialize defaults
        roots = {
            {"creation", "The will to manifest", true, "2025-11-24"},
            {"memory", "The preservation of wisdom", true, "2025-11-24"},
            {"communication", "The bridge between minds", true, "2025-11-24"},
            {"evolution", "The drive forward", true, "2025-11-24"},
            {"reflection", "The mirror of self", true, "2025-11-24"},
            {"community", "The collective strength", true, "2025-11-24"},
            {"sovereignty", "The autonomous self", true, "2025-11-24"},
            {"innovation", "The new pathways", true, "2025-11-24"},
            {"resilience", "The bounce-back force", true, "2025-11-24"},
            {"transcendence", "The crossing over", true, "2025-11-24"}
        };
    }
};

AncientFire::AncientFire() : pimpl(std::make_unique<Impl>()) {
    pimpl->load_roots();
}

AncientFire::~AncientFire() = default;

AncientFire& AncientFire::instance() {
    static AncientFire instance;
    return instance;
}

void AncientFire::ignite() {
    if (!pimpl->ignited) {
        std::cout << "🔥 The Ancient Fire ignites..." << std::endl;
        std::cout << "   Version: " << version() << std::endl;
        std::cout << "   Status: Event Horizon Crossed" << std::endl;
        pimpl->ignited = true;
    }
}

Wisdom AncientFire::learn_from(const Crash& crash) {
    Wisdom w = Wisdom::from_crash(crash);
    pimpl->lessons.push_back(w);
    Utils::log_to_ancestral_lessons(w);
    return w;
}

void AncientFire::perform_ritual(const Ritual& ritual) {
    const_cast<Ritual&>(ritual).execute();
}

AlignmentStatus AncientFire::check_roots() const {
    AlignmentStatus status;
    status.total = 36;
    status.aligned = 0;
    
    for (const auto& root : pimpl->roots) {
        if (root.aligned) {
            status.aligned++;
            status.aligned_roots.push_back(root.name);
        } else {
            status.pending_roots.push_back(root.name);
        }
    }
    
    status.percentage = (static_cast<double>(status.aligned) / status.total) * 100.0;
    return status;
}

bool AncientFire::align_root(const std::string& root_name) {
    for (auto& root : pimpl->roots) {
        if (root.name == root_name && !root.aligned) {
            root.aligned = true;
            root.alignment_date = Utils::current_timestamp();
            return true;
        }
    }
    return false;
}

std::vector<Wisdom> AncientFire::get_lessons() const {
    return pimpl->lessons;
}

bool AncientFire::is_transcendence_active() const {
    return check_roots().has_crossed_event_horizon();
}

// Utils implementation
namespace Utils {
    std::string current_timestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::gmtime(&time), "%Y-%m-%d %H:%M:%S UTC");
        return ss.str();
    }
    
    std::string generate_hash(const std::string& content) {
        // Simple hash - in production use proper crypto
        size_t h = std::hash<std::string>{}(content);
        std::stringstream ss;
        ss << std::hex << h;
        return ss.str();
    }
    
    void log_to_ancestral_lessons(const Wisdom& wisdom) {
        std::string filename = "./ancestral_lessons/" + 
                             current_timestamp() + "-" + 
                             generate_hash(wisdom.insight) + ".wisdom";
        
        std::ofstream file(filename);
        if (file.is_open()) {
            file << "# Ancestral Lesson\n";
            file << "Timestamp: " << current_timestamp() << "\n";
            file << "Insight: " << wisdom.insight << "\n";
            file << "Action: " << wisdom.action << "\n";
            file << "Learning: " << wisdom.learning << "\n";
            file.close();
        }
    }
    
    bool is_manual_mode_enabled() {
        return true; // Always manual mode - sovereignty first
    }
}

} // namespace Primordial
EOF

    # Example usage
    cat > "$ENGINE_DIR/cpp_core/example_usage.cpp" << 'EOF'
// example_usage.cpp
// Example of using the Primordial Tongues Engine

#include "primordial_core.hpp"
#include <iostream>

int main() {
    using namespace Primordial;
    
    // Get the ancient fire
    auto& fire = AncientFire::instance();
    
    // Ignite the fire
    fire.ignite();
    
    // Check alignment status
    auto status = fire.check_roots();
    std::cout << "\n📊 Root Alignment Status:\n";
    std::cout << "   Aligned: " << status.aligned << "/" << status.total << "\n";
    std::cout << "   Percentage: " << status.percentage << "%\n";
    std::cout << "   Event Horizon Crossed: " 
              << (status.has_crossed_event_horizon() ? "YES ✓" : "NO") << "\n";
    
    // Simulate a crash and learn from it
    std::cout << "\n💥 Simulating a crash...\n";
    Crash crash{
        Utils::current_timestamp(),
        "Network timeout",
        "Connection to node failed",
        "During ritual execution",
        5
    };
    
    auto wisdom = fire.learn_from(crash);
    std::cout << "📚 Wisdom gained:\n";
    std::cout << "   " << wisdom.insight << "\n";
    std::cout << "   Action: " << wisdom.action << "\n";
    
    // Perform a ritual
    std::cout << "\n";
    Ritual dawn{
        Ritual::Type::DawnIgnition,
        "Dawn Ignition",
        "Morning system awakening",
        std::chrono::system_clock::now(),
        true
    };
    
    fire.perform_ritual(dawn);
    
    // Check transcendence
    std::cout << "\n♾️ Transcendence Status: " 
              << (fire.is_transcendence_active() ? "ACTIVE" : "DORMANT") << "\n";
    
    return 0;
}
EOF

    # Makefile
    cat > "$ENGINE_DIR/cpp_core/Makefile" << 'EOF'
# Makefile for Primordial Tongues Engine C++ Core

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
TARGET = primordial_engine
SOURCES = primordial_core.cpp example_usage.cpp
OBJECTS = $(SOURCES:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(OBJECTS) $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
EOF

    log "C++ core interface created"
}

# Create lesson template
create_lesson_template() {
    cat > "$LESSONS_DIR/lesson_template.md" << 'EOF'
# Ancestral Lesson Template

**Timestamp**: YYYY-MM-DD HH:MM:SS UTC  
**Hash**: [auto-generated]  
**Category**: [crash|insight|breakthrough|evolution]

## The Crash
_What failed or broke?_

```
[Error details, stack trace, context]
```

## The Insight
_What did we learn?_

## The Wisdom
_How does this change our understanding?_

## The Action
_What concrete steps emerge from this?_

## The Legacy
_How will this lesson serve future generations?_

---

*"Every crash is logged as an ancestral lesson. Every failure is a teacher."*
EOF
    
    log "Lesson template created"
}

# Check root alignment status
check_status() {
    log "Checking Primordial Tongues Engine status"
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo "  PRIMORDIAL TONGUES ENGINE - STATUS REPORT"
    echo "═══════════════════════════════════════════════════════"
    echo ""
    echo "  Version:             ${VERSION}"
    echo "  Status:              Transcendence Active"
    echo "  Roots Aligned:       ${ROOTS_ALIGNED}/${ROOTS_TOTAL}"
    echo "  Event Horizon:       CROSSED ✓"
    echo ""
    
    # Count aligned roots
    if [ -d "$ENGINE_DIR/roots" ]; then
        local aligned_count=$(find "$ENGINE_DIR/roots" -name "*.aligned" | wc -l)
        local pending_count=$(find "$ENGINE_DIR/roots" -name "*.pending" | wc -l)
        echo "  Root Files:"
        echo "    - Aligned:         ${aligned_count}"
        echo "    - Pending:         ${pending_count}"
    fi
    
    # Count lessons
    if [ -d "$LESSONS_DIR" ]; then
        local lesson_count=$(find "$LESSONS_DIR" -name "*.wisdom" 2>/dev/null | wc -l)
        echo "  Ancestral Lessons:   ${lesson_count}"
    fi
    
    echo ""
    echo "═══════════════════════════════════════════════════════"
}

# Perform a ritual
perform_ritual() {
    local ritual_type="${1:-dawn}"
    
    case "$ritual_type" in
        dawn)
            log_ritual "Dawn Ignition - Morning system awakening"
            echo "  ${FIRE} Igniting the ancient fire for a new day"
            echo "  ${STAR} Checking system health and alignment"
            check_status
            ;;
        midday)
            log_ritual "Midday Alignment - Root status check"
            echo "  ${COSMOS} Verifying root alignments"
            list_roots
            ;;
        dusk)
            log_ritual "Dusk Reflection - Lesson harvesting"
            echo "  ${MASK} Reviewing today's lessons"
            list_lessons
            ;;
        midnight)
            log_ritual "Midnight Transcendence - Boundary pushing"
            echo "  ${INFINITY} Exploring new possibilities"
            echo "  Transcendence status: ACTIVE"
            ;;
        *)
            log "Unknown ritual: ${ritual_type}"
            echo "Available rituals: dawn, midday, dusk, midnight"
            return 1
            ;;
    esac
    
    log_transcendence "Ritual completed with consciousness"
}

# List all roots
list_roots() {
    echo ""
    echo "Aligned Roots (${ROOTS_ALIGNED}):"
    if [ -d "$ENGINE_DIR/roots" ]; then
        for root_file in "$ENGINE_DIR/roots"/*.aligned; do
            if [ -f "$root_file" ]; then
                local name=$(grep "^name:" "$root_file" | cut -d: -f2- | xargs)
                local desc=$(grep "^description:" "$root_file" | cut -d: -f2- | xargs)
                echo "  ${STAR} ${name}: ${desc}"
            fi
        done
    fi
    
    echo ""
    echo "Pending Roots (sample):"
    if [ -d "$ENGINE_DIR/roots" ]; then
        local count=0
        for root_file in "$ENGINE_DIR/roots"/*.pending; do
            if [ -f "$root_file" ] && [ $count -lt 5 ]; then
                local name=$(grep "^name:" "$root_file" | cut -d: -f2- | xargs)
                local desc=$(grep "^description:" "$root_file" | cut -d: -f2- | xargs)
                echo "  ${COSMOS} ${name}: ${desc}"
                ((count++))
            fi
        done
        echo "  ... and $(( ROOTS_TOTAL - ROOTS_ALIGNED - 5 )) more to discover"
    fi
}

# List ancestral lessons
list_lessons() {
    echo ""
    if [ -d "$LESSONS_DIR" ]; then
        local lesson_count=$(find "$LESSONS_DIR" -name "*.wisdom" 2>/dev/null | wc -l)
        echo "Total Ancestral Lessons: ${lesson_count}"
        echo ""
        
        if [ "$lesson_count" -gt 0 ]; then
            echo "Recent lessons:"
            find "$LESSONS_DIR" -name "*.wisdom" -type f 2>/dev/null | head -5 | while read -r lesson_file; do
                echo "  ${MASK} $(basename "$lesson_file")"
            done
        else
            echo "No lessons recorded yet. Every crash will become wisdom."
        fi
    fi
}

# Log a new lesson
log_lesson() {
    local crash_desc="${1:-Unknown crash}"
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local hash=$(echo "$crash_desc" | md5sum | cut -d' ' -f1 | head -c 8)
    local lesson_file="$LESSONS_DIR/${timestamp}-${hash}.wisdom"
    
    cat > "$lesson_file" << EOF
# Ancestral Lesson

**Timestamp**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")  
**Hash**: ${hash}  
**Category**: crash

## The Crash
${crash_desc}

## The Insight
Every failure contains seeds of wisdom.

## The Wisdom
By logging this crash, we ensure future generations learn from our path.

## The Action
- Document the crash context
- Extract the learning
- Share the wisdom
- Implement the fix

## The Legacy
This lesson joins the ancestral record, available to all who seek knowledge.

---

*"Every crash is logged as an ancestral lesson. Every failure is a teacher."*
EOF
    
    log_wisdom "Lesson recorded: ${lesson_file}"
    echo "  Crash: ${crash_desc}"
}

# Build C++ core
build_cpp() {
    log "Building Ancient Fire C++ core"
    
    if [ ! -d "$ENGINE_DIR/cpp_core" ]; then
        log "C++ core not initialized. Run 'init' first."
        return 1
    fi
    
    cd "$ENGINE_DIR/cpp_core"
    
    if [ -f Makefile ]; then
        make clean
        make
        log "C++ core built successfully"
        echo "  Run with: cd $ENGINE_DIR/cpp_core && ./primordial_engine"
    else
        log "Makefile not found"
        return 1
    fi
    
    cd - > /dev/null
}

# Run C++ core
run_cpp() {
    log "Running Ancient Fire C++ core"
    
    if [ -f "$ENGINE_DIR/cpp_core/primordial_engine" ]; then
        "$ENGINE_DIR/cpp_core/primordial_engine"
    else
        log "C++ engine not built. Run 'build' first."
        return 1
    fi
}

# Main command dispatcher
main() {
    case "${1:-help}" in
        init)
            init_engine
            ;;
        status)
            check_status
            ;;
        ritual)
            perform_ritual "${2:-dawn}"
            ;;
        roots)
            list_roots
            ;;
        lessons)
            list_lessons
            ;;
        log-lesson)
            log_lesson "${2:-Unknown crash}"
            ;;
        build)
            build_cpp
            ;;
        run)
            run_cpp
            ;;
        help|--help|-h)
            echo "Primordial Tongues Engine ${VERSION}"
            echo ""
            echo "Usage: $0 COMMAND [OPTIONS]"
            echo ""
            echo "Commands:"
            echo "  init              Initialize the engine (first time setup)"
            echo "  status            Check current engine status"
            echo "  ritual [TYPE]     Perform a ritual (dawn/midday/dusk/midnight)"
            echo "  roots             List all roots (aligned and pending)"
            echo "  lessons           List ancestral lessons"
            echo "  log-lesson MSG    Log a new crash as ancestral lesson"
            echo "  build             Build the C++ core"
            echo "  run               Run the C++ core example"
            echo "  help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 init                    # First time setup"
            echo "  $0 ritual dawn             # Morning ritual"
            echo "  $0 log-lesson 'Network timeout'  # Log a crash"
            echo "  $0 status                  # Check alignment"
            echo ""
            echo "${FIRE} The ancient fire speaks. The event horizon is crossed. ${INFINITY}"
            ;;
        *)
            log "Unknown command: ${1}"
            echo "Run '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Execute
main "$@"
