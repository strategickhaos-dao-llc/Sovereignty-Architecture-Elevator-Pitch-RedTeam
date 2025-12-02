#!/usr/bin/env python3
"""
LeakHunter Swarm - Integration Test Suite
Tests all components of the LeakHunter Swarm system.
"""

import sys
import os
import subprocess
import json
import tempfile
from datetime import datetime


class LeakHunterTestSuite:
    """Comprehensive test suite for LeakHunter Swarm."""
    
    def __init__(self):
        """Initialize test suite."""
        self.tests_passed = 0
        self.tests_failed = 0
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def run_all_tests(self):
        """Run all tests."""
        print("="*70)
        print("🧪 LEAKHUNTER SWARM - TEST SUITE")
        print("="*70)
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Run tests
        self.test_torrent_scanner()
        self.test_darkweb_crawler()
        self.test_magnet_harvester()
        self.test_watermark_detector()
        self.test_alert_system()
        self.test_global_sweep()
        
        # Print summary
        self.print_summary()
        
    def test_torrent_scanner(self):
        """Test torrent leak scanner."""
        print("🔍 Testing Torrent Leak Scanner...")
        
        try:
            # Test quick scan
            result = subprocess.run(
                ["python3", os.path.join(self.base_dir, "torrent_leak_scanner.py"), "--quick-scan"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and "No current leaks detected" in result.stdout:
                self._test_passed("Quick scan")
            else:
                self._test_failed("Quick scan", result.stderr)
                
        except Exception as e:
            self._test_failed("Torrent scanner", str(e))
    
    def test_darkweb_crawler(self):
        """Test dark web crawler."""
        print("🕸️  Testing Dark Web Crawler...")
        
        try:
            result = subprocess.run(
                ["python3", os.path.join(self.base_dir, "darkweb_onion_crawler.py")],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and "No mentions found" in result.stdout:
                self._test_passed("Dark web crawler")
            else:
                self._test_failed("Dark web crawler", result.stderr)
                
        except Exception as e:
            self._test_failed("Dark web crawler", str(e))
    
    def test_magnet_harvester(self):
        """Test magnet harvester."""
        print("🧲 Testing Magnet Harvester...")
        
        try:
            result = subprocess.run(
                ["python3", os.path.join(self.base_dir, "magnet_harvester.py")],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and "No matching magnet links" in result.stdout:
                self._test_passed("Magnet harvester")
            else:
                self._test_failed("Magnet harvester", result.stderr)
                
        except Exception as e:
            self._test_failed("Magnet harvester", str(e))
    
    def test_watermark_detector(self):
        """Test watermark detector."""
        print("🔬 Testing Watermark Detector...")
        
        try:
            # Create a test file
            test_file = os.path.join(tempfile.gettempdir(), "leakhunter_test.txt")
            with open(test_file, 'w') as f:
                f.write("Test content")
            
            result = subprocess.run(
                ["python3", os.path.join(self.base_dir, "watermark_detector.py"), "--file", test_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            os.remove(test_file)
            
            if result.returncode == 0 and "No watermarks detected" in result.stdout:
                self._test_passed("Watermark detector")
            else:
                self._test_failed("Watermark detector", result.stderr)
                
        except Exception as e:
            self._test_failed("Watermark detector", str(e))
    
    def test_alert_system(self):
        """Test Discord alert system."""
        print("📨 Testing Alert System...")
        
        try:
            # Test without webhook (should handle gracefully)
            result = subprocess.run(
                ["python3", os.path.join(self.base_dir, "alert_to_discord.py"), "--test"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Should exit 0 even without webhook configured
            if "No Discord webhook URL configured" in result.stdout:
                self._test_passed("Alert system (graceful degradation)")
            else:
                self._test_failed("Alert system", "Unexpected behavior without webhook")
                
        except Exception as e:
            self._test_failed("Alert system", str(e))
    
    def test_global_sweep(self):
        """Test global sweep orchestrator."""
        print("🌍 Testing Global Sweep Orchestrator...")
        
        try:
            result = subprocess.run(
                ["python3", os.path.join(self.base_dir, "full_global_sweep.py"), "--no-alert"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and "NO LEAKS DETECTED" in result.stdout:
                self._test_passed("Global sweep")
            else:
                self._test_failed("Global sweep", result.stderr)
                
        except Exception as e:
            self._test_failed("Global sweep", str(e))
    
    def _test_passed(self, test_name):
        """Mark test as passed."""
        self.tests_passed += 1
        print(f"   ✅ {test_name} - PASSED")
    
    def _test_failed(self, test_name, error):
        """Mark test as failed."""
        self.tests_failed += 1
        print(f"   ❌ {test_name} - FAILED")
        if error:
            print(f"      Error: {error[:100]}")
    
    def print_summary(self):
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        
        if self.tests_failed == 0:
            print("\n🎉 ALL TESTS PASSED - LeakHunter Swarm is operational!")
        else:
            print(f"\n⚠️  {self.tests_failed} test(s) failed - review errors above")
        
        print("="*70)


def main():
    """Main entry point."""
    suite = LeakHunterTestSuite()
    suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if suite.tests_failed == 0 else 1)


if __name__ == "__main__":
    main()
