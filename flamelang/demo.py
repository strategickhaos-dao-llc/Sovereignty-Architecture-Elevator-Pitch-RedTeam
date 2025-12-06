#!/usr/bin/env python3
"""
FlameLang Interactive Demo
Showcases language features
"""
import sys
import time

from core.compiler import FlameLangCompiler
from glyphs.registry import GLYPH_REGISTRY
from physics.engine import ENGINE
from security.sovereignty import PROTOCOL


def print_header(text):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"🔥 {text}")
    print("=" * 70)


def demo_glyphs():
    """Demo 1: Glyph System"""
    print_header("Demo 1: Glyph Registry (17 Glyphs)")
    
    print("\nCore Glyphs:")
    for symbol in ['⚡', '🔥', '🌊', '⚛️', '🎯', '🔮']:
        glyph = GLYPH_REGISTRY[symbol]
        print(f"  {symbol} {glyph['name']:15} @ {glyph['frequency']}Hz")
    
    print("\nPhysics Glyphs:")
    for symbol in ['BH1', 'OC1', 'PS1', 'GR1', 'ED1', 'MT1']:
        glyph = GLYPH_REGISTRY[symbol]
        print(f"  {symbol:3} {glyph['name']:20} @ {glyph['frequency']}Hz")
    
    print("\nSecurity Glyphs:")
    for symbol in ['🛡️', '🔒', '👁️', '⚔️', '🌐']:
        glyph = GLYPH_REGISTRY[symbol]
        print(f"  {symbol} {glyph['name']:15} @ {glyph['frequency']}Hz")
    
    time.sleep(1)


def demo_physics():
    """Demo 2: Physics Engine"""
    print_header("Demo 2: Black Hole Simulation")
    
    solar_mass = 1.989e30  # kg
    radius = 1e7  # 10,000 km
    
    print(f"\n🕳️ Schwarzschild Black Hole Simulation @137Hz")
    print(f"   Mass: {solar_mass:.3e} kg (1 solar mass)")
    print(f"   Observation radius: {radius/1000:.0f} km")
    
    result = ENGINE.compute_schwarzschild(solar_mass, radius)
    
    print(f"\n   Schwarzschild radius: {result['schwarzschild_radius']/1000:.2f} km")
    print(f"   Redshift factor: {result['redshift_factor']:.6f}")
    print(f"   Escape velocity: {result['escape_velocity']/1000:.0f} km/s")
    print(f"   Inside horizon: {result['is_inside_horizon']}")
    
    time.sleep(1)


def demo_sovereignty():
    """Demo 3: Sovereignty Protocol"""
    print_header("Demo 3: Sovereignty Protocol")
    
    # Initialize
    init_result = PROTOCOL.initialize()
    
    print("\n🛡️ Sovereignty Status:")
    print(f"   Network isolated: {init_result['network_isolation']}")
    print(f"   Telemetry detection: {init_result['telemetry_detection']}")
    print(f"   Coherence monitoring: {init_result['coherence_monitoring']}")
    print(f"   Boundary hash: {init_result['boundary_hash'][:32]}...")
    
    # Test telemetry detection
    print("\n🔍 Telemetry Detection Test:")
    test_code = "Connecting to telemetry.microsoft.com for analytics"
    detected = PROTOCOL.detect_telemetry(test_code)
    
    if detected:
        print(f"   ⚠️  Detected {len(detected)} telemetry pattern(s):")
        for pattern in detected:
            print(f"      - {pattern}")
    else:
        print("   ✓ No telemetry detected")
    
    time.sleep(1)


def demo_compiler():
    """Demo 4: Compiler Execution"""
    print_header("Demo 4: FlameLang Compiler")
    
    compiler = FlameLangCompiler()
    
    print("\n📝 Example Program:")
    program = """
# Black hole simulation
sim BH1 M=1.989e30 r=1e7

# Physical constants
c
"""
    print(program)
    
    print("🔥 Execution:")
    result = compiler.compile(program)
    
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.6g}")
            else:
                print(f"   {key}: {value}")
    
    time.sleep(1)


def demo_constants():
    """Demo 5: Physical Constants"""
    print_header("Demo 5: Physical Constants")
    
    print("\n🌌 Built-in Constants:")
    print(f"   c (speed of light):         {ENGINE.constants['c']:,.0f} m/s")
    print(f"   G (gravitational constant): {ENGINE.constants['G']:.6e} m³/kg·s²")
    print(f"   α (fine-structure):         1/{1/ENGINE.constants['alpha']:.0f}")
    print(f"   π (pi):                     {ENGINE.constants['pi']:.10f}")
    print(f"   e (Euler's number):         {ENGINE.constants['e']:.10f}")
    print(f"   φ (golden ratio):           {ENGINE.constants['phi']:.10f}")
    
    time.sleep(1)


def main():
    """Run interactive demo"""
    print("\n" + "=" * 70)
    print("🔥 " + "FlameLang Interactive Demo".center(66) + " 🔥")
    print("=" * 70)
    print("\nShowcasing: Glyphs, Physics, Sovereignty, Compilation")
    print("Press Ctrl+C to skip demos")
    
    try:
        time.sleep(2)
        demo_glyphs()
        demo_physics()
        demo_sovereignty()
        demo_compiler()
        demo_constants()
        
        print("\n" + "=" * 70)
        print("🔥 Demo Complete! 🔥")
        print("=" * 70)
        print("\nTry the REPL: ./flamelang repl")
        print("Run examples: ./flamelang run examples/demo.fl")
        print("\n🔥 Stay sovereign. 🔥\n")
        
    except KeyboardInterrupt:
        print("\n\n🔥 Demo interrupted. Stay sovereign. 🔥\n")
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
