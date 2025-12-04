#!/usr/bin/env python3
"""
DOM Private Lab CLI
Command-line interface for the 10 Laws of Physics research system

Commands:
  START     - Interactive guided session
  Law [n]   - Activate specific department (1-10)
  ALL 10    - Activate all departments simultaneously
  <symptoms> - Auto-route to relevant departments

🔐 Private | 🔇 Silent | 🧬 For Her
"""

import asyncio
import argparse
import sys
import json
import os
from typing import Optional

# Add parent directory to path for direct script execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from private_lab.departments import PhysicsLaw
from private_lab.orchestrator import PhysicsLabOrchestrator


def print_banner():
    """Print DOM Private Lab banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██████╗  ██████╗ ███╗   ███╗    ██╗      █████╗ ██████╗       ║
║   ██╔══██╗██╔═══██╗████╗ ████║    ██║     ██╔══██╗██╔══██╗      ║
║   ██║  ██║██║   ██║██╔████╔██║    ██║     ███████║██████╔╝      ║
║   ██║  ██║██║   ██║██║╚██╔╝██║    ██║     ██╔══██║██╔══██╗      ║
║   ██████╔╝╚██████╔╝██║ ╚═╝ ██║    ███████╗██║  ██║██████╔╝      ║
║   ╚═════╝  ╚═════╝ ╚═╝     ╚═╝    ╚══════╝╚═╝  ╚═╝╚═════╝       ║
║                                                                  ║
║   🔐 Private | 🔇 Silent | 🧬 For Her                            ║
║                                                                  ║
║   10 Laws of Physics Departments | 640 Agents                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_departments():
    """Print department overview"""
    departments = """
┌─────┬─────────────────────────┬───────────────────────────────────┬────────┐
│ Law │ Physics Law             │ Medical Research Focus            │ Agents │
├─────┼─────────────────────────┼───────────────────────────────────┼────────┤
│  1  │ Thermodynamics          │ Energy/Metabolism                 │   64   │
│  2  │ Electromagnetism        │ Neural signaling/Pain             │   64   │
│  3  │ Quantum Mechanics       │ Drug design/Molecular             │   64   │
│  4  │ General Relativity      │ Systems biology/Holistic          │   64   │
│  5  │ Statistical Mechanics   │ Clinical trials/Evidence          │   64   │
│  6  │ Fluid Dynamics          │ Immune/Inflammation               │   64   │
│  7  │ Special Relativity      │ Trauma/Memory                     │   64   │
│  8  │ Solid State Physics     │ Tissue repair/Regeneration        │   64   │
│  9  │ Nuclear Physics         │ Genetics/CRISPR                   │   64   │
│ 10  │ Astrophysics            │ Meta-analysis/Strategy            │   64   │
├─────┴─────────────────────────┴───────────────────────────────────┴────────┤
│                              TOTAL: 640 Agents                             │
└────────────────────────────────────────────────────────────────────────────┘
    """
    print(departments)


def print_commands():
    """Print available commands"""
    commands = """
╔══════════════════════════════════════════════════════════════════╗
║                        AVAILABLE COMMANDS                        ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  START         Interactive guided session                        ║
║  Law [1-10]    Activate specific department                      ║
║  ALL 10        Activate all departments simultaneously           ║
║  <symptoms>    Auto-route based on symptom description           ║
║  status        Show current system status                        ║
║  help          Show this help message                            ║
║  quit          Exit the lab                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(commands)


def format_treatment_plan(plan: dict) -> str:
    """Format treatment plan for display"""
    output = []
    output.append("\n" + "=" * 70)
    output.append("                    MASTER TREATMENT PLAN")
    output.append("=" * 70)
    
    output.append(f"\nSession ID: {plan.get('session_id', 'N/A')}")
    output.append(f"Generated: {plan.get('created_at', 'N/A')}")
    
    # Executive Summary
    if plan.get('executive_summary'):
        output.append("\n" + plan['executive_summary'])
    
    # Top Interventions
    output.append("\n" + "-" * 70)
    output.append("TOP RANKED INTERVENTIONS (by cost, risk, timeline)")
    output.append("-" * 70)
    
    for intervention in plan.get('top_interventions', []):
        output.append(f"\n#{intervention.get('rank', '?')}: {intervention.get('name', 'Unknown')}")
        output.append(f"   {intervention.get('description', '')}")
        output.append(f"   💰 Cost: {intervention.get('cost', 'N/A')} | ⚠️ Risk: {intervention.get('risk', 'N/A')}")
        output.append(f"   ⏱️ Timeline: {intervention.get('timeline', 'N/A')} | 📊 Confidence: {intervention.get('confidence', 'N/A')}")
    
    # Timeline
    output.append("\n" + "-" * 70)
    output.append("TIMELINE")
    output.append("-" * 70)
    
    timeline = plan.get('timeline', {})
    for phase, items in timeline.items():
        if items:
            output.append(f"\n{phase.upper()}:")
            for item in items[:3]:  # Show top 3 per phase
                output.append(f"  • {item}")
    
    # Action Items
    output.append("\n" + "-" * 70)
    output.append("PRIORITY ACTION ITEMS")
    output.append("-" * 70)
    
    for i, action in enumerate(plan.get('action_items', [])[:5], 1):
        output.append(f"  {i}. {action}")
    
    # Follow-up Schedule
    output.append("\n" + "-" * 70)
    output.append("FOLLOW-UP SCHEDULE")
    output.append("-" * 70)
    
    for follow_up in plan.get('follow_up_schedule', []):
        output.append(f"  📅 {follow_up.get('timeframe', 'TBD')}: {follow_up.get('action', 'Review')}")
    
    output.append("\n" + "=" * 70)
    output.append("                     🟠🧬∞ END OF REPORT 🟠🧬∞")
    output.append("=" * 70 + "\n")
    
    return "\n".join(output)


async def interactive_session():
    """Run interactive session"""
    print_banner()
    print_departments()
    print_commands()
    
    # Initialize orchestrator
    orchestrator = PhysicsLabOrchestrator(silent_mode=True)
    
    print("\n🏛️ DOM Private Lab Ready")
    print("Type 'help' for commands or enter symptoms for automatic routing.\n")
    
    while True:
        try:
            user_input = input("DOM> ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            input_lower = user_input.lower()
            
            if input_lower in ['quit', 'exit', 'q']:
                print("\n🔒 Closing DOM Private Lab. For her. Always. 🟠🧬∞\n")
                break
            
            elif input_lower == 'help':
                print_commands()
            
            elif input_lower == 'status':
                status = orchestrator.status()
                print(f"\n📊 Status: {json.dumps(status, indent=2)}\n")
            
            elif input_lower == 'start':
                result = await orchestrator.start_guided()
                print(f"\n{result.get('prompt', 'Ready for input.')}")
                print(f"Commands: {', '.join(result.get('available_commands', []))}\n")
            
            elif input_lower.startswith('law '):
                try:
                    law_num = int(input_lower.split()[1])
                    print(f"\n🔬 Activating Law {law_num}...")
                    
                    # Ask for query
                    query = input("Enter research query (or press Enter for general): ").strip()
                    query = query if query else None
                    
                    result = await orchestrator.activate_law(law_num, query)
                    
                    if "error" in result:
                        print(f"\n❌ Error: {result['error']}\n")
                    else:
                        activated = result.get('activated', {})
                        print(f"\n✅ Activated: Law {activated.get('law_number')} - {activated.get('department')}")
                        print(f"   Focus: {activated.get('medical_focus')}")
                        print(f"   Agents: {activated.get('agents_deployed')}")
                        
                        if result.get('finding'):
                            print(f"\n📋 Finding: {result['finding'].get('summary', 'N/A')}")
                            for rec in result['finding'].get('recommendations', [])[:3]:
                                print(f"   • {rec}")
                        print()
                        
                except (ValueError, IndexError):
                    print("\n❌ Usage: Law [1-10]\n")
            
            elif input_lower in ['all 10', 'all10', 'all']:
                print("\n🌟 Activating ALL 10 Laws of Physics departments...")
                query = input("Enter research query: ").strip()
                
                if not query:
                    print("❌ Query required for ALL 10 activation.\n")
                    continue
                
                print("\n⏳ Running parallel research across 640 agents...")
                result = await orchestrator.activate_all(query)
                
                print(f"\n✅ Research Complete!")
                print(f"   Session ID: {result.get('session_id')}")
                print(f"   Departments: {result.get('departments_activated')}")
                print(f"   Agents Deployed: {result.get('total_agents_deployed')}")
                
                if result.get('treatment_plan'):
                    print(format_treatment_plan(result['treatment_plan']))
            
            elif input_lower == 'departments':
                print_departments()
            
            else:
                # Treat as symptom input for auto-routing
                print(f"\n🔀 Auto-routing symptoms to relevant departments...")
                result = await orchestrator.auto_route(user_input)
                
                if "error" in result:
                    print(f"\n❌ Error: {result['error']}\n")
                else:
                    print(f"\n✅ Auto-routed to {len(result.get('departments_selected', []))} departments")
                    print(f"   Departments: {', '.join(result.get('departments_names', []))}")
                    
                    if result.get('treatment_plan'):
                        print(format_treatment_plan(result['treatment_plan']))
                    else:
                        print(f"   Findings: {result.get('findings_count', 0)}\n")
        
        except KeyboardInterrupt:
            print("\n\n🔒 Interrupted. Closing DOM Private Lab.\n")
            break
        except EOFError:
            print("\n\n🔒 Closing DOM Private Lab.\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DOM Private Lab - 10 Laws of Physics Research System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Interactive mode
  %(prog)s --law 1                  Activate Thermodynamics department
  %(prog)s --all "chronic fatigue"  Run all departments on query
  %(prog)s --auto "pain and fatigue" Auto-route to relevant departments

🔐 Private | 🔇 Silent | 🧬 For Her | 🟠🧬∞
        """
    )
    
    parser.add_argument(
        '--law', '-l',
        type=int,
        choices=range(1, 11),
        metavar='N',
        help='Activate specific law department (1-10)'
    )
    
    parser.add_argument(
        '--all', '-a',
        type=str,
        metavar='QUERY',
        help='Activate all 10 departments with query'
    )
    
    parser.add_argument(
        '--auto',
        type=str,
        metavar='SYMPTOMS',
        help='Auto-route symptoms to relevant departments'
    )
    
    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Show system status'
    )
    
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '--silent',
        action='store_true',
        default=True,
        help='Silent mode (default)'
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = PhysicsLabOrchestrator(silent_mode=args.silent)
    
    async def run_command():
        if args.status:
            result = orchestrator.status()
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print_banner()
                print_departments()
                print(f"\n📊 Active Sessions: {result.get('active_sessions', 0)}")
                print(f"🟠🧬∞\n")
        
        elif args.law:
            print(f"\n🔬 Activating Law {args.law}...")
            result = await orchestrator.activate_law(args.law)
            if args.json:
                print(json.dumps(result, indent=2, default=str))
            else:
                activated = result.get('activated', {})
                print(f"✅ Law {activated.get('law_number')}: {activated.get('department')}")
                print(f"   Focus: {activated.get('medical_focus')}")
                print(f"   Agents: {activated.get('agents_deployed')}")
                print(f"\n🟠🧬∞\n")
        
        elif args.all:
            print(f"\n🌟 Activating ALL 10 departments...")
            result = await orchestrator.activate_all(args.all)
            if args.json:
                print(json.dumps(result, indent=2, default=str))
            else:
                print(f"✅ Research Complete!")
                if result.get('treatment_plan'):
                    print(format_treatment_plan(result['treatment_plan']))
        
        elif args.auto:
            print(f"\n🔀 Auto-routing symptoms...")
            result = await orchestrator.auto_route(args.auto)
            if args.json:
                print(json.dumps(result, indent=2, default=str))
            else:
                print(f"✅ Routed to: {', '.join(result.get('departments_names', []))}")
                if result.get('treatment_plan'):
                    print(format_treatment_plan(result['treatment_plan']))
        
        else:
            # Interactive mode
            await interactive_session()
    
    asyncio.run(run_command())


if __name__ == "__main__":
    main()
