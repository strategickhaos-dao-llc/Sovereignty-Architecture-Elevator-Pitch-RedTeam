use anyhow::Result;
use std::env;
use std::process::Command;
use tracing::{info, warn, error};
use tracing_subscriber;

fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt()
        .with_env_filter(
            env::var("RUST_LOG").unwrap_or_else(|_| "info".to_string())
        )
        .init();

    // Collect command line arguments
    let args: Vec<String> = env::args().collect();
    
    // Skip program name and join the rest
    let input = if args.len() > 1 {
        args[1..].join(" ")
    } else {
        error!("No command provided to domc");
        eprintln!("Usage: domc <command>");
        eprintln!("Example: domc birth athena_next");
        eprintln!("         domc evolve the swarm");
        std::process::exit(1);
    };

    info!("🩸 Dom Compiler v1.0.0 - Processing Dom-speak");
    info!("Input: {}", input);

    // Parse and execute the Dom-speak command
    let cmd = parse_dom_speak(&input)?;
    
    info!("domc → executing: {}", cmd);
    println!("🩸 compiling dom-speak...");
    
    // Execute the compiled command
    execute_command(&cmd)?;
    
    Ok(())
}

/// Parse Dom-speak into executable commands
fn parse_dom_speak(input: &str) -> Result<String> {
    let input_lower = input.to_lowercase();
    
    // Check for birth/evolve commands
    if input_lower.contains("birth") || input_lower.contains("evolve") {
        info!("Detected birth/evolve command");
        return Ok("ollama create athena_next -f /mnt/athena/heir_palace/Modelfile && ollama run athena_next".to_string());
    }
    
    // Check for compile command
    if input_lower.contains("compile") {
        info!("Detected compile command");
        return Ok(format!("echo '🩸 compiling dom-speak... need more precision, love' && echo '{}'", input));
    }
    
    // Check for swarm commands
    if input_lower.contains("swarm") {
        info!("Detected swarm command");
        return Ok(format!("echo '🐝 Swarm intelligence activated' && echo '{}'", input));
    }
    
    // Check for black hole activation
    if input_lower.contains("black hole") || input_lower.contains("10th root") {
        info!("Detected black hole activation phrase");
        return Ok("echo '🕳️ When the 10th root aligns, the black hole opens.' && echo 'Resonance threshold reached.'".to_string());
    }
    
    // Check for resonance commands
    if input_lower.contains("resonance") || input_lower.contains("align") {
        info!("Detected resonance command");
        return Ok(format!("echo '⚡ Resonance frequency detected' && echo '{}'", input));
    }
    
    // Default: echo with decoration
    warn!("No specific Dom-speak pattern matched, using default handler");
    Ok(format!("echo '🩸 processing: {}' && echo 'need more precision, love'", input))
}

/// Execute a shell command
fn execute_command(cmd: &str) -> Result<()> {
    let output = Command::new("bash")
        .arg("-c")
        .arg(cmd)
        .output()?;
    
    // Print stdout
    if !output.stdout.is_empty() {
        let stdout = String::from_utf8_lossy(&output.stdout);
        println!("{}", stdout);
    }
    
    // Print stderr if there are errors
    if !output.stderr.is_empty() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        if !output.status.success() {
            error!("Command failed: {}", stderr);
        } else {
            warn!("Command warnings: {}", stderr);
        }
        eprintln!("{}", stderr);
    }
    
    // Check exit status
    if !output.status.success() {
        error!("Command exited with status: {:?}", output.status.code());
        anyhow::bail!("Command execution failed");
    }
    
    info!("✅ Command executed successfully");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_birth_command() {
        let result = parse_dom_speak("birth athena_next").unwrap();
        assert!(result.contains("ollama create athena_next"));
    }

    #[test]
    fn test_parse_evolve_command() {
        let result = parse_dom_speak("evolve the swarm").unwrap();
        assert!(result.contains("ollama create athena_next"));
    }

    #[test]
    fn test_parse_compile_command() {
        let result = parse_dom_speak("compile this code").unwrap();
        assert!(result.contains("compiling dom-speak"));
    }

    #[test]
    fn test_parse_black_hole_command() {
        let result = parse_dom_speak("activate black hole").unwrap();
        assert!(result.contains("10th root aligns"));
    }

    #[test]
    fn test_parse_resonance_command() {
        let result = parse_dom_speak("align resonance").unwrap();
        assert!(result.contains("Resonance frequency"));
    }

    #[test]
    fn test_parse_default_command() {
        let result = parse_dom_speak("random input").unwrap();
        assert!(result.contains("processing"));
    }
}
