#!/usr/bin/env python3
"""
Hogwarts Protocol Test Suite
Unit tests for the data models and business logic
"""

import hashlib
import sys
from datetime import datetime, timezone
from decimal import Decimal
import uuid

# Add parent directory to path
sys.path.insert(0, '.')

from hogwarts_protocol.models import (
    Student, Course, Assignment, Spell, CFTBalance, CFTTransaction,
    RevenueRoute, SpellLicense, SpellStatus, CFTTransactionType, 
    RevenueRouteType, create_default_revenue_routes, DEFAULT_REVENUE_SPLIT
)


class HogwartsProtocolTests:
    """Test suite for Hogwarts Protocol models"""
    
    def __init__(self):
        self.results = []
    
    def _test(self, name: str, condition: bool, details: str = ""):
        """Record test result"""
        status = "PASS" if condition else "FAIL"
        self.results.append({
            "name": name,
            "status": status,
            "details": details
        })
        icon = "✅" if condition else "❌"
        print(f"  {icon} {name}")
        if not condition and details:
            print(f"      Details: {details}")
        return condition
    
    def run_all(self):
        """Run all test categories"""
        print("\n🏰 HOGWARTS PROTOCOL TEST SUITE")
        print("=" * 50)
        
        self.test_student_model()
        self.test_course_model()
        self.test_assignment_model()
        self.test_spell_model()
        self.test_cft_balance_model()
        self.test_cft_transaction_model()
        self.test_revenue_routes()
        self.test_spell_license_model()
        self.test_enums()
        self.test_serialization()
        self.test_content_hashing()
        
        self.print_summary()
        return all(r['status'] == 'PASS' for r in self.results)
    
    def test_student_model(self):
        """Test Student entity creation and validation"""
        print("\n📚 Student Model Tests")
        
        # Test default creation
        student = Student()
        self._test(
            "Student - default creation",
            student.student_id is not None and len(student.student_id) == 36,
            f"Generated ID: {student.student_id}"
        )
        
        self._test(
            "Student - default values",
            student.is_active == True and student.total_spells == 0,
            f"is_active={student.is_active}, total_spells={student.total_spells}"
        )
        
        # Test with parameters
        student2 = Student(
            edu_email="dom@snhu.edu",
            edu_institution="SNHU",
            display_name="Dom",
            wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f8eabc"
        )
        self._test(
            "Student - with parameters",
            student2.edu_email == "dom@snhu.edu" and student2.wallet_address is not None,
            f"email={student2.edu_email}"
        )
        
        # Test to_dict
        data = student2.to_dict()
        self._test(
            "Student - to_dict serialization",
            'student_id' in data and 'created_at' in data,
            f"Keys: {list(data.keys())[:5]}..."
        )
    
    def test_course_model(self):
        """Test Course entity creation"""
        print("\n📖 Course Model Tests")
        
        course = Course(
            course_code="MAT-243",
            course_name="Applied Statistics",
            institution="SNHU"
        )
        
        self._test(
            "Course - creation with code",
            course.course_code == "MAT-243",
            f"course_code={course.course_code}"
        )
        
        self._test(
            "Course - default platform",
            course.platform == "CourseQuest Hogwarts",
            f"platform={course.platform}"
        )
        
        self._test(
            "Course - default xp_multiplier",
            course.xp_multiplier == Decimal("1.0"),
            f"xp_multiplier={course.xp_multiplier}"
        )
        
        self._test(
            "Course - instructor_share_pct",
            course.instructor_share_pct == Decimal("0.10"),
            f"instructor_share_pct={course.instructor_share_pct}"
        )
    
    def test_assignment_model(self):
        """Test Assignment entity creation"""
        print("\n📝 Assignment Model Tests")
        
        assignment = Assignment(
            course_id="test-course-id",
            assignment_name="Project One",
            assignment_code="P1",
            base_xp=120
        )
        
        self._test(
            "Assignment - creation",
            assignment.assignment_name == "Project One",
            f"name={assignment.assignment_name}"
        )
        
        self._test(
            "Assignment - base_xp",
            assignment.base_xp == 120,
            f"base_xp={assignment.base_xp}"
        )
        
        self._test(
            "Assignment - max_grade_bonus",
            assignment.max_grade_bonus == Decimal("0.5"),
            f"max_grade_bonus={assignment.max_grade_bonus}"
        )
    
    def test_spell_model(self):
        """Test Spell entity creation"""
        print("\n🔮 Spell Model Tests")
        
        spell = Spell(
            owner_id="test-owner-id",
            spell_name="spell_descriptive_stats.py",
            spell_type="python"
        )
        
        self._test(
            "Spell - creation",
            spell.spell_name == "spell_descriptive_stats.py",
            f"name={spell.spell_name}"
        )
        
        self._test(
            "Spell - default status",
            spell.status == SpellStatus.DRAFT,
            f"status={spell.status.value}"
        )
        
        self._test(
            "Spell - default cft_minted",
            spell.cft_minted == Decimal("0"),
            f"cft_minted={spell.cft_minted}"
        )
        
        # Test content hash
        test_content = b"def hello(): return 'world'"
        computed_hash = spell.compute_content_hash(test_content)
        expected_hash = hashlib.sha256(test_content).hexdigest()
        
        self._test(
            "Spell - content hash computation",
            spell.content_hash == expected_hash and len(computed_hash) == 64,
            f"hash={computed_hash[:20]}..."
        )
        
        # Test on-chain record
        on_chain = spell.to_on_chain_record()
        self._test(
            "Spell - on_chain_record structure",
            'spell_id' in on_chain and 'content_hash' in on_chain and 'platform' in on_chain,
            f"Keys: {list(on_chain.keys())}"
        )
    
    def test_cft_balance_model(self):
        """Test CFTBalance entity"""
        print("\n💰 CFT Balance Model Tests")
        
        balance = CFTBalance(
            student_id="test-student-id",
            available_balance=Decimal("100.5"),
            staked_balance=Decimal("50.25")
        )
        
        self._test(
            "CFTBalance - total_balance property",
            balance.total_balance == Decimal("150.75"),
            f"total={balance.total_balance}"
        )
        
        self._test(
            "CFTBalance - governance_weight property",
            balance.governance_weight == Decimal("50.25"),
            f"weight={balance.governance_weight}"
        )
        
        # Test serialization
        data = balance.to_dict()
        self._test(
            "CFTBalance - to_dict includes computed",
            'total_balance' in data and 'governance_weight' in data,
            f"total_balance={data['total_balance']}"
        )
    
    def test_cft_transaction_model(self):
        """Test CFTTransaction entity"""
        print("\n📜 CFT Transaction Model Tests")
        
        transaction = CFTTransaction(
            student_id="test-student-id",
            transaction_type=CFTTransactionType.MINT,
            amount=Decimal("120"),
            reference_type="spell",
            reference_id="test-spell-id",
            reason="Earned CFT for verified spell: B+"
        )
        
        self._test(
            "CFTTransaction - creation",
            transaction.amount == Decimal("120"),
            f"amount={transaction.amount}"
        )
        
        self._test(
            "CFTTransaction - transaction_type",
            transaction.transaction_type == CFTTransactionType.MINT,
            f"type={transaction.transaction_type.value}"
        )
        
        # Test serialization
        data = transaction.to_dict()
        self._test(
            "CFTTransaction - to_dict",
            data['transaction_type'] == 'mint' and data['amount'] == '120',
            f"type={data['transaction_type']}"
        )
    
    def test_revenue_routes(self):
        """Test revenue routing configuration"""
        print("\n💸 Revenue Routes Tests")
        
        # Test default split totals to 100
        total = sum(DEFAULT_REVENUE_SPLIT.values())
        self._test(
            "RevenueRoutes - default split totals 100%",
            total == Decimal("100"),
            f"total={total}%"
        )
        
        # Test default route creation
        routes = create_default_revenue_routes(
            spell_id="test-spell-id",
            creator_id="test-creator-id",
            creator_address="0x742d35Cc6634C0532925a3b844Bc9e7595f8eabc"
        )
        
        self._test(
            "RevenueRoutes - creates 4 routes",
            len(routes) == 4,
            f"routes={len(routes)}"
        )
        
        creator_route = next(r for r in routes if r.route_type == RevenueRouteType.CREATOR)
        self._test(
            "RevenueRoutes - creator gets 60%",
            creator_route.percentage == Decimal("60"),
            f"creator_pct={creator_route.percentage}"
        )
        
        charity_route = next(r for r in routes if r.route_type == RevenueRouteType.CHARITY)
        self._test(
            "RevenueRoutes - charity (ValorYield) gets 10%",
            charity_route.percentage == Decimal("10"),
            f"charity_pct={charity_route.percentage}"
        )
    
    def test_spell_license_model(self):
        """Test SpellLicense entity"""
        print("\n📄 Spell License Model Tests")
        
        license_ = SpellLicense(
            spell_id="test-spell-id",
            licensor_id="test-owner-id",
            licensee_id="test-buyer-id",
            price_paid=Decimal("25.00"),
            payment_currency="USD"
        )
        
        self._test(
            "SpellLicense - creation",
            license_.price_paid == Decimal("25.00"),
            f"price={license_.price_paid}"
        )
        
        self._test(
            "SpellLicense - default payment_processor",
            license_.payment_processor == "stripe",
            f"processor={license_.payment_processor}"
        )
        
        self._test(
            "SpellLicense - default license_type",
            license_.license_type == "educational",
            f"type={license_.license_type}"
        )
    
    def test_enums(self):
        """Test enum values"""
        print("\n🏷️ Enum Tests")
        
        self._test(
            "SpellStatus - has all values",
            len(SpellStatus) == 5,
            f"values={[s.value for s in SpellStatus]}"
        )
        
        self._test(
            "CFTTransactionType - has all values",
            len(CFTTransactionType) == 7,
            f"values={[t.value for t in CFTTransactionType]}"
        )
        
        self._test(
            "RevenueRouteType - has all values",
            len(RevenueRouteType) == 5,
            f"values={[r.value for r in RevenueRouteType]}"
        )
    
    def test_serialization(self):
        """Test JSON serialization of all models"""
        print("\n📦 Serialization Tests")
        
        import json
        
        # Student
        student = Student(edu_email="test@edu.com")
        try:
            json.dumps(student.to_dict())
            self._test("Serialization - Student", True)
        except Exception as e:
            self._test("Serialization - Student", False, str(e))
        
        # Course
        course = Course(course_code="TEST-101", course_name="Test Course")
        try:
            json.dumps(course.to_dict())
            self._test("Serialization - Course", True)
        except Exception as e:
            self._test("Serialization - Course", False, str(e))
        
        # Spell
        spell = Spell(owner_id="test", spell_name="test.py")
        try:
            json.dumps(spell.to_dict())
            self._test("Serialization - Spell", True)
        except Exception as e:
            self._test("Serialization - Spell", False, str(e))
        
        # CFTBalance
        balance = CFTBalance(student_id="test")
        try:
            json.dumps(balance.to_dict())
            self._test("Serialization - CFTBalance", True)
        except Exception as e:
            self._test("Serialization - CFTBalance", False, str(e))
    
    def test_content_hashing(self):
        """Test content hash integrity"""
        print("\n🔒 Content Hashing Tests")
        
        spell1 = Spell(owner_id="test", spell_name="test.py")
        spell2 = Spell(owner_id="test", spell_name="test.py")
        
        content = b"print('Hello Hogwarts')"
        hash1 = spell1.compute_content_hash(content)
        hash2 = spell2.compute_content_hash(content)
        
        self._test(
            "Content hash - deterministic",
            hash1 == hash2,
            f"hash1={hash1[:16]}... hash2={hash2[:16]}..."
        )
        
        different_content = b"print('Different')"
        hash3 = Spell(owner_id="test", spell_name="test.py").compute_content_hash(different_content)
        
        self._test(
            "Content hash - different for different content",
            hash1 != hash3,
            f"hash1={hash1[:16]}... hash3={hash3[:16]}..."
        )
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = total - passed
        
        print(f"   Total: {total}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {failed}")
        print(f"   Pass Rate: {passed/total:.1%}")
        
        if failed > 0:
            print("\n   Failed Tests:")
            for r in self.results:
                if r['status'] == 'FAIL':
                    print(f"      ❌ {r['name']}")
        
        status = "✅ ALL TESTS PASSED" if failed == 0 else f"❌ {failed} TESTS FAILED"
        print(f"\n{status}")
        print("=" * 50)


def main():
    """Main entry point"""
    tests = HogwartsProtocolTests()
    success = tests.run_all()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
