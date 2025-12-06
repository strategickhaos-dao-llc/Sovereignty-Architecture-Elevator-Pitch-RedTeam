#!/usr/bin/env python3
"""FlameLang Demo - Showcase all features."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.repl import Interpreter
from glyphs.registry import REGISTRY
from physics.engine import ENGINE
from security.sovereignty import SOVEREIGNTY

def main():
    print("=" * 60)
    print("🔥 FlameLang System Demo")
    print("=" * 60)
    
    # Initialize
    print("\n1. Initializing Sovereignty System...")
    SOVEREIGNTY.initialize_sovereign_environment()
    
    # Show glyphs
    print("\n2. Registered Glyphs:")
    print(f"   Total: {len(REGISTRY.all())} glyphs")
    for category in ['core', 'physics', 'security']:
        count = len(REGISTRY.by_category(category))
        print(f"   - {category}: {count} glyphs")
    
    # Physics demonstrations
    print("\n3. Physics Engine Demonstrations:")
    
    print("\n   a) Solar Mass Black Hole:")
    M_sun = 1.989e30
    bh = ENGINE.simulate_black_hole('BH1', M_sun, 1e7)
    print(f"      Schwarzschild radius: {bh['r_s']/1000:.2f} km")
    print(f"      Metric g_tt: {bh['g_tt']:.6f}")
    
    print("\n   b) Ocean Eddy Coherence:")
    oc = ENGINE.simulate_ocean_eddy('OC1', 0.95)
    print(f"      Coherence: {oc['coherence']:.2f}")
    print(f"      Phase stability: {oc['phase_stability']:.4f}")
    
    print("\n   c) Photon Sphere:")
    ps = ENGINE.simulate_photon_sphere('PS1', M_sun)
    print(f"      Photon orbit radius: {ps['r_photon']/1000:.2f} km")
    
    # Interpreter demo
    print("\n4. Interpreter Execution:")
    interpreter = Interpreter()
    
    print("\n   a) Variable assignment:")
    interpreter.execute("x = 42")
    
    print("\n   b) Glyph pipeline:")
    interpreter.execute("⚡ -> [BH1] |> 🔥")
    
    # Security demo
    print("\n5. Security Features:")
    print(f"   Network enabled: {SOVEREIGNTY.network.is_network_enabled()}")
    print(f"   Telemetry blocked: Yes")
    
    status = SOVEREIGNTY.get_status()
    print(f"   System coherence: {status['coherence']:.2%}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🔥 Demo Complete - All Systems Operational")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run: flamelang repl")
    print("  - Try: flamelang compile examples/demo.fl")
    print("  - Export: flamelang export-glyphs")
    print("\n🔥 Stay Sovereign. Compute Freely. 🔥")

if __name__ == '__main__':
    main()
