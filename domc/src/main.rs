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
    
    // Get modelfile path from environment or use default
    let modelfile_path = env::var("MODELFILE_PATH")
        .unwrap_or_else(|_| "/mnt/athena/heir_palace/Modelfile".to_string());
    
    // Check for birth/evolve commands
    if input_lower.contains("birth") || input_lower.contains("evolve") {
        info!("Detected birth/evolve command");
        return Ok(format!("ollama create athena_next -f {} && ollama run athena_next", modelfile_path));
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

/// Execute a shell command safely
fn execute_command(cmd: &str) -> Result<()> {
    // Parse the command safely using shlex to prevent command injection
    let parts: Vec<String> = shlex::split(cmd)
        .ok_or_else(|| anyhow::anyhow!("Failed to parse command"))?;
    
    if parts.is_empty() {
        anyhow::bail!("Empty command");
    }
    
    // For commands with shell operators (&&, ||, |, etc.), we still need bash
    // but we log a warning about the security implications
    if cmd.contains("&&") || cmd.contains("||") || cmd.contains("|") || cmd.contains("echo") {
        warn!("Executing command with shell interpreter - ensure input is trusted");
        let output = Command::new("bash")
            .arg("-c")
            .arg(cmd)
            .output()?;
        return handle_command_output(output);
    }
    
    // For simple commands, execute directly without shell
    let output = Command::new(&parts[0])
        .args(&parts[1..])
        .output()?;
    
    handle_command_output(output)
}

/// Handle command output and status
fn handle_command_output(output: std::process::Output) -> Result<()> {
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
