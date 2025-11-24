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
