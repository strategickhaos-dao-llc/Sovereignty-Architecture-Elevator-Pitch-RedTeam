#include "primordial_vectors.hpp"
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * STRATEGICKHAOS SOLVERN — THE PRIMORDIAL COMPILER
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * The black-hole keyspace decryption oracle.
 * 
 * This solvern reads runtime entropy (session data, chat logs, spite markers)
 * and checks for resonance with the 36 primordial vectors from the Egyptian-
 * Hebrew stellar calendar.
 * 
 * If ≥10 vectors align → Event Horizon opens → Full system unlocks
 * If <10 vectors → Decoy response → Access denied
 * 
 * Usage:
 *   ./solvern <entropy_file>         # Check entropy from file
 *   ./solvern -s "entropy string"    # Check entropy from string
 *   ./solvern --test                 # Run self-test
 * 
 * Empire Eternal. 🔥
 * ═══════════════════════════════════════════════════════════════════════════
 */

namespace {

const std::string DECOY_MESSAGE = R"(
╔═══════════════════════════════════════════════════════════════════════════╗
║                     POSITIVE PSYCHOLOGY CODEX                             ║
║                           (Decoy Layer)                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

Access Denied: Insufficient entropy resonance detected.

The system requires ancestral spite-frequency calibration.
Current resonance level does not meet the 10/36 threshold.

Suggestion: Try again when you've descended through the Duat.

😏 "They never saw the pivot coming."
)";

const std::string UNLOCK_MESSAGE = R"(
╔═══════════════════════════════════════════════════════════════════════════╗
║                     BLACK HOLE EVENT HORIZON                              ║
║                          UNLOCKED ✨                                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

✨ RESONANCE ACHIEVED ✨

The 36-dimensional Egyptian-Hebrew keyspace has aligned.
Primordial vectors synchronized with runtime entropy.
Black-pharma layer decrypting...

🔥 As above, so below — compiled. 🔥

Full v9 genome access: GRANTED
Empire Eternal.

From the Duat to the dean's office in one compile cycle.
)";

void print_usage(const char* program_name) {
    std::cout << "Usage:\n"
              << "  " << program_name << " <entropy_file>         # Check entropy from file\n"
              << "  " << program_name << " -s \"entropy string\"    # Check entropy from string\n"
              << "  " << program_name << " --test                 # Run self-test\n"
              << "  " << program_name << " --help                 # Show this help\n"
              << std::endl;
}

std::string read_file(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

void run_self_test() {
    std::cout << "═══════════════════════════════════════════════════════════════════════════\n"
              << "SOLVERN SELF-TEST — Primordial Vector Database\n"
              << "═══════════════════════════════════════════════════════════════════════════\n\n";
    
    // Test 1: No resonance
    std::string test1 = "This is ordinary text with no special markers.";
    uint64_t count1 = solvern::count_resonances(test1);
    std::cout << "Test 1 - Low entropy: " << count1 << "/36 vectors matched";
    std::cout << (count1 < 10 ? " ✓ PASS" : " ✗ FAIL") << "\n\n";
    
    // Test 2: Partial resonance (< 10)
    std::string test2 = "VEH YELI SIT MAH HET HAZ HRI LAU MELH";
    uint64_t count2 = solvern::count_resonances(test2);
    std::cout << "Test 2 - Partial resonance: " << count2 << "/36 vectors matched";
    std::cout << (count2 == 9 ? " ✓ PASS" : " ✗ FAIL") << "\n\n";
    
    // Test 3: Full resonance (≥ 10)
    std::string test3 = "VEH YELI SIT ELM MAH LEH AKA KAH HET HAZ ELD LAV HAH YZL";
    uint64_t count3 = solvern::count_resonances(test3);
    bool resonates3 = solvern::black_hole_resonance(test3);
    std::cout << "Test 3 - Strong resonance: " << count3 << "/36 vectors matched, "
              << "Black hole: " << (resonates3 ? "OPEN" : "CLOSED");
    std::cout << (resonates3 ? " ✓ PASS" : " ✗ FAIL") << "\n\n";
    
    // Test 4: All vectors
    std::stringstream test4_stream;
    for (const auto& vec : solvern::primordial_vectors) {
        test4_stream << vec << " ";
    }
    std::string test4 = test4_stream.str();
    uint64_t count4 = solvern::count_resonances(test4);
    std::cout << "Test 4 - Maximum resonance: " << count4 << "/36 vectors matched";
    std::cout << (count4 == 36 ? " ✓ PASS" : " ✗ FAIL") << "\n\n";
    
    std::cout << "═══════════════════════════════════════════════════════════════════════════\n"
              << "Self-test complete. Empire Eternal. 🔥\n"
              << "═══════════════════════════════════════════════════════════════════════════\n";
}

void check_entropy(const std::string& entropy, bool verbose = false) {
    uint64_t resonance_count = solvern::count_resonances(entropy);
    bool unlocked = solvern::black_hole_resonance(entropy);
    
    std::cout << "\n═══════════════════════════════════════════════════════════════════════════\n"
              << "ENTROPY ANALYSIS\n"
              << "═══════════════════════════════════════════════════════════════════════════\n\n";
    
    std::cout << "Entropy length: " << entropy.length() << " characters\n";
    std::cout << "Resonance count: " << resonance_count << "/36 vectors\n";
    std::cout << "Threshold: 10/36 (spark of life)\n";
    std::cout << "Status: " << (unlocked ? "UNLOCKED ✨" : "LOCKED 🔒") << "\n\n";
    
    if (verbose) {
        std::cout << "Matched vectors:\n";
        for (const auto& root : solvern::primordial_vectors) {
            if (solvern::vector_matches(entropy, root)) {
                std::cout << "  ✓ " << root << "\n";
            }
        }
        std::cout << "\n";
    }
    
    std::cout << "═══════════════════════════════════════════════════════════════════════════\n";
    
    if (unlocked) {
        std::cout << UNLOCK_MESSAGE << std::endl;
    } else {
        std::cout << DECOY_MESSAGE << std::endl;
    }
}

} // anonymous namespace

int main(int argc, char* argv[]) {
    try {
        if (argc < 2) {
            print_usage(argv[0]);
            return 1;
        }
        
        std::string arg = argv[1];
        
        if (arg == "--help" || arg == "-h") {
            print_usage(argv[0]);
            return 0;
        }
        
        if (arg == "--test") {
            run_self_test();
            return 0;
        }
        
        if (arg == "-s" || arg == "--string") {
            if (argc < 3) {
                std::cerr << "Error: -s option requires an entropy string argument\n";
                return 1;
            }
            std::string entropy = argv[2];
            check_entropy(entropy, true);
            return 0;
        }
        
        // Default: treat argument as filename
        std::string entropy = read_file(arg);
        check_entropy(entropy, true);
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
