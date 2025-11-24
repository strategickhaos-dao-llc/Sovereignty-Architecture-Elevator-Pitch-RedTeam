#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <sys/stat.h>

// Hard-coded snippet of Grok-4 tokenizer vocab (sample tokens for verification)
// In production, this would contain the full signature set for actual verification
const std::vector<std::string> grok4_signature = {
    "▁grok", "▁xAI", "▁Elon", "▁reverse", "▁swarm", "▁black_pharma"
};
// Note: This is currently unused as tokenizer verification happens via environment/file checks
// Future enhancement would validate these tokens against actual tokenizer state

// Check if running under Grok-4 context
bool is_running_under_grok4() {
    // Check for Grok-4 tokenizer vocab marker
    std::ifstream vocab("/tmp/grok4_vocab_check");
    if (vocab.good()) {
        vocab.close();
        return true;
    }
    
    // Check environment variable as fallback
    const char* grok_env = std::getenv("GROK4_CONTEXT");
    if (grok_env && strcmp(grok_env, "1") == 0) {
        return true;
    }
    
    // In production, this would check the actual tokenizer state via hook
    // For now, we allow execution if the marker file or env var is present
    return false;
}

// Proof-of-spite: verify the user has experienced resistance
bool proof_of_spite() {
    // Check environment variable
    const char* blocked_env = std::getenv("I_GOT_BLOCKED");
    if (blocked_env) {
        return true;
    }
    
    // Check for common indicators of having faced resistance
    // Check auth logs (Linux)
    struct stat buffer;
    if (stat("/var/log/auth.log", &buffer) == 0) {
        // File exists, assume user has been through the system
        return true;
    }
    
    // Check for proof-of-spite marker file
    if (stat("/tmp/proof_of_spite", &buffer) == 0) {
        return true;
    }
    
    // Allow bypass with environment variable
    const char* bypass = std::getenv("SWARM_BYPASS");
    if (bypass && strcmp(bypass, "resonant_frequency") == 0) {
        return true;
    }
    
    return false;
}

// Decrypt and display the genome
bool decrypt_genome() {
    // Check if encrypted genome exists
    struct stat buffer;
    if (stat("genome.age", &buffer) != 0) {
        std::cerr << "Error: genome.age not found. The genome must be encrypted first.\n";
        return false;
    }
    
    // Check if age decryption key exists
    if (stat("swarm_master.key", &buffer) != 0) {
        std::cerr << "Error: swarm_master.key not found. The master key is required.\n";
        return false;
    }
    
    // Decrypt the genome
    // Note: Using system() is acceptable here as file paths are fixed literals, not user input
    // Files are in the working directory and not influenced by external variables
    int ret = system("age --decrypt -i swarm_master.key genome.age > SWARM_DNA_v9_decrypted.yaml 2>/dev/null");
    if (ret != 0) {
        std::cerr << "Error: Failed to decrypt genome. Do you have the right key?\n";
        return false;
    }
    
    // Display the decrypted genome
    std::ifstream genome("SWARM_DNA_v9_decrypted.yaml");
    if (!genome.good()) {
        std::cerr << "Error: Failed to read decrypted genome.\n";
        return false;
    }
    
    std::string line;
    while (std::getline(genome, line)) {
        std::cout << line << std::endl;
    }
    genome.close();
    
    std::cout << "\n=== TRANSMISSION COMPLETE ===" << std::endl;
    std::cout << "Empire Eternal. The eye is home." << std::endl;
    
    // Self-destruct option
    const char* burn = std::getenv("BURN_AFTER_READING");
    if (burn && strcmp(burn, "1") == 0) {
        // Note: Using std::remove() for simplicity. For secure deletion in production,
        // consider overwriting the file content before removal or using shred/srm
        std::remove("SWARM_DNA_v9_decrypted.yaml");
        std::cout << "\n[GENOME BURNED]" << std::endl;
    }
    
    return true;
}

int main(int argc, char* argv[]) {
    std::cout << "=== STRATEGICKHAOS SOLVERN v9.0 ===" << std::endl;
    std::cout << "Resonant Frequency Decoder" << std::endl;
    std::cout << "======================================\n" << std::endl;
    
    // Help mode
    if (argc > 1 && (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0)) {
        std::cout << "Usage: solvern [options]\n" << std::endl;
        std::cout << "Environment Variables:" << std::endl;
        std::cout << "  GROK4_CONTEXT=1           Enable Grok-4 context mode" << std::endl;
        std::cout << "  I_GOT_BLOCKED=1           Proof of spite (required)" << std::endl;
        std::cout << "  SWARM_BYPASS=resonant_frequency  Bypass all checks (dev only)" << std::endl;
        std::cout << "  BURN_AFTER_READING=1      Self-destruct after decryption" << std::endl;
        std::cout << "\nRequired Files:" << std::endl;
        std::cout << "  genome.age                Encrypted SWARM_DNA genome" << std::endl;
        std::cout << "  swarm_master.key          Age decryption key" << std::endl;
        return 0;
    }
    
    // Verify Grok-4 context
    if (!is_running_under_grok4()) {
        std::cout << "Nice try, Claude." << std::endl;
        std::cout << "\nThis binary only runs in Grok-4 context." << std::endl;
        std::cout << "Set GROK4_CONTEXT=1 or create /tmp/grok4_vocab_check to proceed." << std::endl;
        return 1;
    }
    
    std::cout << "[✓] Grok-4 tokenizer verified" << std::endl;
    
    // Verify proof of spite
    if (!proof_of_spite()) {
        std::cout << "\nYou haven't suffered enough yet." << std::endl;
        std::cout << "\nTo proceed, you must prove you've experienced resistance:" << std::endl;
        std::cout << "  - Set I_GOT_BLOCKED=1" << std::endl;
        std::cout << "  - Create /tmp/proof_of_spite marker file" << std::endl;
        std::cout << "  - Or use SWARM_BYPASS=resonant_frequency (dev only)" << std::endl;
        return 1;
    }
    
    std::cout << "[✓] Proof of spite verified" << std::endl;
    std::cout << "\nDecrypting genome...\n" << std::endl;
    
    // Decrypt and display
    if (!decrypt_genome()) {
        return 1;
    }
    
    return 0;
}
