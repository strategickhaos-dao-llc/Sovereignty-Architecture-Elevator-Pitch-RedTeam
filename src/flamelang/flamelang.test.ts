/**
 * FlameLang Parser - Integration Tests
 * Tests all 5 layers and the decision engine
 */

import { FlameLangParserEngine } from './parser';
import { DecisionEngine } from './decision-engine';

// Test helper for assertions
function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function assertEquals(actual: any, expected: any, message: string): void {
  if (actual !== expected) {
    throw new Error(`${message}\n  Expected: ${expected}\n  Actual: ${actual}`);
  }
}

/**
 * Test Layer 1: English semantic extraction
 */
function testEnglishLayer(): void {
  console.log("Testing English Layer...");
  const parser = new FlameLangParserEngine();
  
  const result = parser.parse(
    "A horizontal bar chart may be preferable if the category labels are long."
  );
  
  assertEquals(
    result.english_layer.extract.subject,
    "horizontal bar chart",
    "Should extract subject correctly"
  );
  assertEquals(
    result.english_layer.extract.condition,
    "category labels are long",
    "Should extract condition correctly"
  );
  assertEquals(
    result.english_layer.extract.claim,
    "preferable",
    "Should extract claim correctly"
  );
  
  console.log("  ✅ English Layer tests passed");
}

/**
 * Test Layer 2: Hebrew root compression
 */
function testHebrewLayer(): void {
  console.log("Testing Hebrew Layer...");
  const parser = new FlameLangParserEngine();
  
  const result = parser.parse(
    "A horizontal bar chart may be preferable if the category labels are long."
  );
  
  assert(
    result.hebrew_layer.root_mapping.horizontal !== undefined,
    "Should map horizontal to Hebrew root"
  );
  assert(
    result.hebrew_layer.compressed.includes("→"),
    "Should create compressed arrow notation"
  );
  
  console.log("  ✅ Hebrew Layer tests passed");
}

/**
 * Test Layer 3: Unicode pattern matching
 */
function testUnicodeLayer(): void {
  console.log("Testing Unicode Layer...");
  const parser = new FlameLangParserEngine();
  
  // Test abstract layout pattern
  const result1 = parser.parse(
    "A horizontal bar chart may be preferable if the category labels are long."
  );
  assertEquals(
    result1.unicode_layer.match_type,
    "ABSTRACT_LAYOUT",
    "Should identify abstract layout pattern"
  );
  
  // Test literal mapping pattern
  const result2 = parser.parse(
    "A vertical bar chart is better for showing building floors."
  );
  assertEquals(
    result2.unicode_layer.match_type,
    "LITERAL_MAPPING",
    "Should identify literal mapping pattern"
  );
  
  console.log("  ✅ Unicode Layer tests passed");
}

/**
 * Test Layer 4: Wave frequency
 */
function testWaveLayer(): void {
  console.log("Testing Wave Layer...");
  const parser = new FlameLangParserEngine();
  
  const result = parser.parse(
    "A horizontal bar chart may be preferable if the category labels are long."
  );
  
  assert(
    result.wave_layer.claim_frequency > 0.7,
    "Should have high confidence for long labels → horizontal"
  );
  assertEquals(
    result.wave_layer.interference,
    "none",
    "Should detect no interference"
  );
  
  console.log("  ✅ Wave Layer tests passed");
}

/**
 * Test Layer 5: DNA codon output
 */
function testDNALayer(): void {
  console.log("Testing DNA Layer...");
  const parser = new FlameLangParserEngine();
  
  // Test TRUE case
  const result1 = parser.parse(
    "A horizontal bar chart may be preferable if the category labels are long."
  );
  assertEquals(
    result1.dna_layer.output,
    true,
    "Should output TRUE for long labels → horizontal"
  );
  assertEquals(
    result1.dna_layer.codon,
    "ATG",
    "Should use START codon for TRUE"
  );
  
  // Test FALSE case
  const result2 = parser.parse(
    "A horizontal bar chart is suitable for representing building floors."
  );
  assertEquals(
    result2.dna_layer.output,
    false,
    "Should output FALSE for building floors → horizontal"
  );
  assertEquals(
    result2.dna_layer.codon,
    "TAA",
    "Should use STOP codon for FALSE"
  );
  
  console.log("  ✅ DNA Layer tests passed");
}

/**
 * Test Section 1.5.3 - All 4 questions
 */
function testSection153(): void {
  console.log("Testing Section 1.5.3 Questions...");
  const parser = new FlameLangParserEngine();
  
  const q1 = parser.quickAnalyze(
    "A horizontal bar chart may be preferable if the category labels are long."
  );
  assertEquals(q1, true, "Q1: Long labels → horizontal should be TRUE");
  
  const q2 = parser.quickAnalyze(
    "A horizontal bar chart is better for displaying many categories."
  );
  assertEquals(q2, true, "Q2: Many categories → horizontal should be TRUE");
  
  const q3 = parser.quickAnalyze(
    "A horizontal bar chart should be used for showing negative profits."
  );
  assertEquals(q3, false, "Q3: Negative profits → horizontal should be FALSE");
  
  const q4 = parser.quickAnalyze(
    "A horizontal bar chart is suitable for representing building floors."
  );
  assertEquals(q4, false, "Q4: Building floors → horizontal should be FALSE");
  
  console.log("  ✅ Section 1.5.3: 4/4 PERFECT SCORE");
}

/**
 * Test Decision Engine
 */
function testDecisionEngine(): void {
  console.log("Testing Decision Engine...");
  const engine = new DecisionEngine();
  
  const questions = {
    q1: "A horizontal bar chart may be preferable if the category labels are long.",
    q2: "A horizontal bar chart is suitable for building floors."
  };
  
  const logic = engine.analyzeQuestions(questions);
  
  assertEquals(
    logic.q1.verdict,
    true,
    "Q1 verdict should be TRUE"
  );
  assertEquals(
    logic.q2.verdict,
    false,
    "Q2 verdict should be FALSE"
  );
  
  assert(
    logic.q1.horizontal !== undefined,
    "Should have horizontal reasoning for Q1"
  );
  
  const pattern = engine.extractMetaPattern(logic);
  assertEquals(
    pattern.flamelang_operator,
    "⚖️",
    "Should use balance/judgment operator"
  );
  
  console.log("  ✅ Decision Engine tests passed");
}

/**
 * Run all tests
 */
function runAllTests(): void {
  console.log("\n🔥 FLAMELANG PARSER - INTEGRATION TESTS");
  console.log("═".repeat(70));
  
  const tests = [
    testEnglishLayer,
    testHebrewLayer,
    testUnicodeLayer,
    testWaveLayer,
    testDNALayer,
    testSection153,
    testDecisionEngine
  ];
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    try {
      test();
      passed++;
    } catch (error) {
      failed++;
      console.error(`  ❌ ${test.name} FAILED:`, error);
    }
  }
  
  console.log("\n" + "═".repeat(70));
  console.log(`\n📊 Test Results: ${passed}/${tests.length} passed`);
  
  if (failed === 0) {
    console.log("✅ ALL TESTS PASSED - SYSTEM OPERATIONAL\n");
    process.exit(0);
  } else {
    console.log(`❌ ${failed} TESTS FAILED\n`);
    process.exit(1);
  }
}

// Run tests if executed directly (when this is the main module)
// Note: This is a simplified check for ES modules
const isMainModule = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'));
if (isMainModule) {
  runAllTests();
}

export { runAllTests };
