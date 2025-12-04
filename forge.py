#!/usr/bin/env python3
"""
Strategickhaos Ingot Forge
===========================

The forge is a "smelter" that dynamically loads and executes ingot modules.
Ingots are modular, self-contained code blocks that can be imported into any project.

Usage:
    python forge.py                    # Run example_ingot
    python forge.py <ingot_name>       # Run a specific ingot
    python forge.py --list             # List all available ingots

Example:
    >>> from forge import load_ingot
    >>> fn = load_ingot("example_ingot")
    >>> fn("Strategickhaos Baby")
    {'input': 'Strategickhaos Baby', 'length': 19, 'is_numeric': False}
"""

import argparse
import importlib
import sys
from pathlib import Path

import yaml


def get_ingot_manifest(name: str) -> dict:
    """
    Load and return the manifest for an ingot.

    Args:
        name: Name of the ingot

    Returns:
        dict: The ingot's manifest data

    Raises:
        FileNotFoundError: If the manifest doesn't exist
        yaml.YAMLError: If the manifest is invalid
    """
    manifest_path = Path(__file__).parent / "ingots" / name / "manifest.yaml"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_ingot(name: str):
    """
    Load an ingot by name and return its main function.

    Args:
        name: Name of the ingot (directory name under /ingots/)

    Returns:
        callable: The ingot's main function as specified in manifest

    Raises:
        FileNotFoundError: If the ingot manifest doesn't exist
        ImportError: If the ingot module can't be imported
        AttributeError: If the function doesn't exist in the module
    """
    manifest = get_ingot_manifest(name)

    # Get module path from manifest, defaulting to src.main
    module_path = manifest.get("api", {}).get("module", "src.main")

    # Import the module
    module = importlib.import_module(f"ingots.{name}.{module_path}")

    # Get the function specified in the manifest
    fn_name = manifest["api"]["function"]
    return getattr(module, fn_name)


def list_ingots() -> list:
    """
    List all available ingots in the ingots directory.

    Returns:
        list: List of dictionaries containing ingot info
    """
    ingots_dir = Path(__file__).parent / "ingots"
    ingots = []

    if not ingots_dir.exists():
        return ingots

    for ingot_path in ingots_dir.iterdir():
        if ingot_path.is_dir() and not ingot_path.name.startswith("_"):
            manifest_path = ingot_path / "manifest.yaml"
            if manifest_path.exists():
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = yaml.safe_load(f)
                        ingots.append({
                            "name": manifest.get("name", ingot_path.name),
                            "version": manifest.get("version", "unknown"),
                            "description": manifest.get("description", "No description"),
                            "path": str(ingot_path)
                        })
                except (yaml.YAMLError, IOError):
                    # Skip ingots with invalid manifests
                    pass

    return ingots


def print_ingots():
    """Print a formatted list of available ingots."""
    ingots = list_ingots()

    if not ingots:
        print("No ingots found in the forge.")
        return

    print("\n🔥 Strategickhaos Ingot Forge")
    print("=" * 50)
    print(f"\nAvailable Ingots ({len(ingots)}):\n")

    for ingot in ingots:
        print(f"  ⚔️  {ingot['name']} v{ingot['version']}")
        print(f"      {ingot['description']}")
        print()

    print("=" * 50)
    print("Usage: python forge.py <ingot_name>")


def main():
    """Main entry point for the forge CLI."""
    parser = argparse.ArgumentParser(
        description="Strategickhaos Ingot Forge - Load and execute modular code blocks"
    )
    parser.add_argument(
        "ingot",
        nargs="?",
        default="example_ingot",
        help="Name of the ingot to load (default: example_ingot)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available ingots"
    )
    parser.add_argument(
        "--input", "-i",
        default="Strategickhaos Baby",
        help="Input data to process (default: 'Strategickhaos Baby')"
    )

    args = parser.parse_args()

    if args.list:
        print_ingots()
        return 0

    try:
        print(f"🔥 Loading ingot: {args.ingot}")
        fn = load_ingot(args.ingot)
        result = fn(args.input)
        print(f"✅ Result: {result}")
        return 0
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nUse --list to see available ingots")
        return 1
    except (ImportError, AttributeError) as e:
        print(f"❌ Error loading ingot: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
