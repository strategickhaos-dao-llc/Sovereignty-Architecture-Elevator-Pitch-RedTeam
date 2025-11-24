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
void Ritual::execute() const {
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
    ritual.execute();
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
