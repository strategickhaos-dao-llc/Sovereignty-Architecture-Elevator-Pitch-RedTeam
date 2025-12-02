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
    
    void execute() const;
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
