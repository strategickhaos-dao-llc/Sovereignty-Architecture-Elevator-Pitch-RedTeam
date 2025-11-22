#!/usr/bin/env python3
"""
Strategickhaos Master Control Panel
Big Picture Menu - November 22, 2025

A unified control panel for managing the entire Strategickhaos ecosystem.
This interactive menu provides quick access to all major components and services.
"""

import os
import subprocess
import sys
from pathlib import Path

# Menu definition: key -> (description, command/url)
MENU = {
    "1": ("🤖 Open Strategickhaos_AI WebUI (Open-WebUI)", "http://localhost:3000"),
    "2": ("🔥 Start Uncensored RedTeam Lab", "docker compose -f AI_RedTeam_Lab/docker-compose.yml up -d"),
    "3": ("🧠 Quantum Symbolic AI Emulator", "code quantum-symbolic-ai-emulator"),
    "4": ("⚡ StrategicKhaos Compiler REPL", "python Strategickhaos_Compiler/src/repl.py"),
    "5": ("🛡️ Honeypot Gate (invite-only)", "http://localhost:8080"),
    "6": ("🗣️ Voice AI Interface", "http://localhost:7850"),
    "7": ("📈 Live Output Stream", "tail -f Strategickhaos_AI/output_stream.md"),
    "8": ("🗺️ Open Obsidian Vault", "start obsidian://open?vault=Strategickhaos_Master_Vault"),
    "9": ("🔒 Open Tailscale-secured Lab", "start https://login.tailscale.com"),
    "0": ("🚀 Nuclear Option – Wipe & Rebuild Everything", "docker compose down -v && git reset --hard && git clean -fdx"),
}

def clear_screen():
    """Clear the terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    """Print the main header"""
    print("=" * 70)
    print("🌌 STRATEGICKHAOS MASTER CONTROL PANEL – November 22, 2025")
    print("=" * 70)
    print()

def print_menu():
    """Display the menu options"""
    for key, (description, _) in MENU.items():
        print(f"{key}. {description}")
    print("\nq. Quit")
    print()

def execute_command(cmd: str, description: str):
    """Execute a command or open a URL"""
    # Detect if this is a URL or special protocol
    is_url = cmd.startswith("http://") or cmd.startswith("https://") or cmd.startswith("obsidian://")
    
    # Handle Windows-specific "start" prefix
    if cmd.startswith("start "):
        is_url = True
        if os.name == "nt":
            # On Windows, use the command as-is
            cmd = cmd
        else:
            # On non-Windows, strip "start" prefix and extract URL
            cmd = cmd[6:].strip()
    
    if is_url:
        # Handle URLs and special protocols
        if os.name == "nt":
            # Windows - use 'start' command
            subprocess.run(f"start {cmd}", shell=True)
        elif sys.platform == "darwin":
            # macOS - use 'open' command
            subprocess.run(["open", cmd], shell=True)
        else:
            # Linux/Unix - use 'xdg-open' command
            subprocess.run(["xdg-open", cmd], shell=True)
        print(f"✅ Opened in default application: {description}")
    else:
        # Execute shell command
        print(f"🚀 Executing: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=False)
        except Exception as e:
            print(f"❌ Error executing command: {e}")

def confirm_nuclear_option():
    """Special confirmation for destructive operations"""
    print("\n⚠️  WARNING: This will wipe and rebuild everything!")
    print("   - Docker containers will be removed")
    print("   - Git repository will be reset")
    print("   - All uncommitted changes will be lost")
    print()
    response = input("Type 'CONFIRM' to proceed: ").strip()
    return response == "CONFIRM"

def main():
    """Main menu loop"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("» Choose your destiny: ").strip().lower()
        
        if choice == "q":
            print("\n🌊 Exiting Strategickhaos Master Control Panel")
            print("May chaos serve your sovereignty.\n")
            break
        
        if choice in MENU:
            desc, cmd = MENU[choice]
            print(f"\n🎯 Launching → {desc}")
            
            # Special handling for nuclear option
            if choice == "0":
                if not confirm_nuclear_option():
                    print("\n❌ Nuclear option cancelled.")
                    input("\nPress Enter to continue...")
                    continue
            
            execute_command(cmd, desc)
            
            # Don't pause for tail command (option 7) as it's blocking
            if choice != "7":
                input("\nPress Enter to continue...")
        else:
            print("\n❌ Invalid choice – try again, chaos agent.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🌊 Interrupted by user. Exiting gracefully.")
        print("May chaos serve your sovereignty.\n")
        sys.exit(0)
