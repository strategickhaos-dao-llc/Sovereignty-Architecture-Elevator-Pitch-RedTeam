#!/usr/bin/env python3
"""
validate_100_layers.py - Validation script for 100-Layer Ascension Protocol

This script validates the 100-layer architecture configuration to ensure:
- All 100 layers are accounted for
- No duplicate layer numbers
- Valid technology references
- Proper dependency chains
- Configuration consistency
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Set


class LayerValidator:
    """Validates the 100-layer architecture configuration"""
    
    def __init__(self, config_path: str = "100_layer_config.yaml"):
        self.config_path = Path(config_path)
        self.config = None
        self.errors = []
        self.warnings = []
        
    def load_config(self) -> bool:
        """Load the YAML configuration file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"Configuration file not found: {self.config_path}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return False
    
    def validate_layer_count(self) -> bool:
        """Validate that exactly 100 layers are defined"""
        if not self.config:
            return False
        
        categories = self.config.get('categories', [])
        total_layers = 0
        layer_numbers = set()
        
        for category in categories:
            layers = category.get('layers', [])
            for layer in layers:
                layer_num = layer.get('number')
                if layer_num:
                    total_layers += 1
                    if layer_num in layer_numbers:
                        self.errors.append(f"Duplicate layer number: {layer_num}")
                    layer_numbers.add(layer_num)
        
        if total_layers != 100:
            self.errors.append(f"Expected 100 layers, found {total_layers}")
            return False
        
        # Check for missing layer numbers
        expected_layers = set(range(1, 101))
        missing_layers = expected_layers - layer_numbers
        if missing_layers:
            self.errors.append(f"Missing layer numbers: {sorted(missing_layers)}")
            return False
        
        print(f"✓ Layer count validation passed: {total_layers} layers")
        return True
    
    def validate_category_ranges(self) -> bool:
        """Validate that category ranges are consistent with layer numbers"""
        if not self.config:
            return False
        
        categories = self.config.get('categories', [])
        all_valid = True
        
        for category in categories:
            range_spec = category.get('range', [])
            if len(range_spec) != 2:
                self.errors.append(f"Invalid range specification in category: {category.get('name')}")
                all_valid = False
                continue
            
            start_range, end_range = range_spec
            layers = category.get('layers', [])
            
            for layer in layers:
                layer_num = layer.get('number')
                if layer_num and not (start_range <= layer_num <= end_range):
                    self.errors.append(
                        f"Layer {layer_num} ({layer.get('name')}) is outside "
                        f"category range {start_range}-{end_range}"
                    )
                    all_valid = False
        
        if all_valid:
            print("✓ Category range validation passed")
        return all_valid
    
    def validate_dependencies(self) -> bool:
        """Validate that all dependency references are valid"""
        if not self.config:
            return False
        
        categories = self.config.get('categories', [])
        category_ids = set(cat.get('id') for cat in categories)
        all_valid = True
        
        integrations = self.config.get('integrations', [])
        for integration in integrations:
            source = integration.get('source')
            target = integration.get('target')
            
            if source != 'all' and source not in category_ids:
                self.warnings.append(f"Integration references unknown source: {source}")
            
            if target != 'all' and target not in category_ids:
                self.warnings.append(f"Integration references unknown target: {target}")
        
        if all_valid:
            print("✓ Dependency validation passed")
        return all_valid
    
    def validate_metadata(self) -> bool:
        """Validate that required metadata is present"""
        if not self.config:
            return False
        
        architecture = self.config.get('architecture', {})
        required_fields = ['name', 'version', 'code', 'status', 'total_layers']
        
        all_valid = True
        for field in required_fields:
            if field not in architecture:
                self.errors.append(f"Missing required architecture field: {field}")
                all_valid = False
        
        total_layers = architecture.get('total_layers')
        if total_layers and total_layers != 100:
            self.errors.append(f"Architecture total_layers should be 100, found {total_layers}")
            all_valid = False
        
        if all_valid:
            print("✓ Metadata validation passed")
        return all_valid
    
    def validate_status_values(self) -> bool:
        """Validate that status values are from allowed set"""
        if not self.config:
            return False
        
        allowed_statuses = {'planned', 'in_progress', 'research', 'complete', 'documentation_complete'}
        categories = self.config.get('categories', [])
        
        all_valid = True
        for category in categories:
            cat_status = category.get('status')
            if cat_status and cat_status not in allowed_statuses:
                self.warnings.append(
                    f"Category '{category.get('name')}' has non-standard status: {cat_status}"
                )
            
            layers = category.get('layers', [])
            for layer in layers:
                layer_status = layer.get('status')
                if layer_status and layer_status not in allowed_statuses:
                    self.warnings.append(
                        f"Layer {layer.get('number')} has non-standard status: {layer_status}"
                    )
        
        print("✓ Status value validation passed")
        return all_valid
    
    def generate_report(self) -> str:
        """Generate a validation report"""
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("100-Layer Ascension Protocol - Validation Report")
        report_lines.append("=" * 70)
        report_lines.append("")
        
        if self.config:
            architecture = self.config.get('architecture', {})
            report_lines.append(f"Architecture: {architecture.get('name', 'Unknown')}")
            report_lines.append(f"Version: {architecture.get('version', 'Unknown')}")
            report_lines.append(f"Code: {architecture.get('code', 'Unknown')}")
            report_lines.append(f"Status: {architecture.get('status', 'Unknown')}")
            report_lines.append("")
            
            categories = self.config.get('categories', [])
            report_lines.append(f"Categories: {len(categories)}")
            
            total_layers = sum(len(cat.get('layers', [])) for cat in categories)
            report_lines.append(f"Total Layers: {total_layers}")
            report_lines.append("")
        
        if self.errors:
            report_lines.append("ERRORS:")
            for error in self.errors:
                report_lines.append(f"  ✗ {error}")
            report_lines.append("")
        
        if self.warnings:
            report_lines.append("WARNINGS:")
            for warning in self.warnings:
                report_lines.append(f"  ⚠ {warning}")
            report_lines.append("")
        
        if not self.errors and not self.warnings:
            report_lines.append("✓ All validations passed successfully!")
            report_lines.append("")
            report_lines.append("The 100-Layer Ascension Protocol configuration is valid.")
        elif self.errors:
            report_lines.append("✗ Validation failed with errors.")
            report_lines.append("")
            report_lines.append("Please fix the errors above and run validation again.")
        else:
            report_lines.append("✓ Validation passed with warnings.")
            report_lines.append("")
            report_lines.append("Review the warnings above for potential issues.")
        
        report_lines.append("")
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)
    
    def validate_all(self) -> bool:
        """Run all validations"""
        print("Validating 100-Layer Ascension Protocol configuration...")
        print()
        
        if not self.load_config():
            return False
        
        validations = [
            self.validate_metadata,
            self.validate_layer_count,
            self.validate_category_ranges,
            self.validate_status_values,
            self.validate_dependencies,
        ]
        
        all_passed = True
        for validation in validations:
            if not validation():
                all_passed = False
        
        print()
        print(self.generate_report())
        
        return all_passed and not self.errors


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate 100-Layer Ascension Protocol configuration"
    )
    parser.add_argument(
        '--config',
        default='100_layer_config.yaml',
        help='Path to configuration file (default: 100_layer_config.yaml)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    validator = LayerValidator(args.config)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
