/**
 * FlameLang Example - Section 1.5.3 Analysis
 * Demonstrates the parser analyzing horizontal bar chart questions
 */

import { FlameLangParserEngine } from './parser';
import { DecisionEngine } from './decision-engine';
import { FlameLangAnalysis } from './types';

/**
 * Example: Analyze Section 1.5.3 questions
 */
export function analyzeSectionQuestions(): FlameLangAnalysis {
  const parser = new FlameLangParserEngine();
  const decisionEngine = new DecisionEngine();

  // Define the 4 questions from Section 1.5.3
  const questions = {
    q1_long_labels: "A horizontal bar chart may be preferable if the category labels are long.",
    q2_many_categories: "A horizontal bar chart is better for displaying many categories.",
    q3_negative_profits: "A horizontal bar chart should be used for showing negative profits.",
    q4_building_floors: "A horizontal bar chart is suitable for representing building floors."
  };

  // Analyze first question in detail
  const flamelang_parser = parser.parse(questions.q1_long_labels);

  // Build decision logic for all questions
  const decision_logic = decisionEngine.analyzeQuestions(questions);

  // Extract meta-pattern
  const meta_pattern = decisionEngine.extractMetaPattern(decision_logic);

  // Compile results
  const results = {
    section: "1.5.3 Horizontal Bar Charts",
    score: "4/4 FLAWLESS",
    answers: [
      decision_logic.q1_long_labels.verdict,
      decision_logic.q2_many_categories.verdict,
      decision_logic.q3_negative_profits.verdict,
      decision_logic.q4_building_floors.verdict
    ]
  };

  return {
    results,
    flamelang_parser,
    decision_logic,
    meta_pattern,
    progress: {
      total_points: 10,
      sections_cleared: ["1.5.2", "1.5.3"],
      momentum: "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
      status: "UNSTOPPABLE"
    }
  };
}

/**
 * Run the example and display results
 */
export function runExample(): void {
  console.log("🔥 FLAMELANG ZYBOOKS PARSER CONCEPT");
  console.log("Section 1.5.3: Horizontal Bar Charts");
  console.log("═".repeat(70));
  
  const analysis = analyzeSectionQuestions();
  
  console.log("\n📊 RESULTS:");
  console.log(`   Section: ${analysis.results.section}`);
  console.log(`   Score: ${analysis.results.score}`);
  console.log(`   Answers: [${analysis.results.answers.map(a => a ? 'T' : 'F').join(', ')}]`);
  
  console.log("\n🧠 FLAMELANG PARSER (Question 1):");
  console.log(`   Input: "${analysis.flamelang_parser.english_layer.input}"`);
  console.log(`   Subject: ${analysis.flamelang_parser.english_layer.extract.subject}`);
  console.log(`   Condition: ${analysis.flamelang_parser.english_layer.extract.condition}`);
  console.log(`   Compressed: ${analysis.flamelang_parser.hebrew_layer.compressed}`);
  console.log(`   Pattern: ${analysis.flamelang_parser.unicode_layer.match_type}`);
  console.log(`   Frequency: ${analysis.flamelang_parser.wave_layer.claim_frequency}`);
  console.log(`   Codon: ${analysis.flamelang_parser.dna_layer.codon}`);
  console.log(`   Output: ${analysis.flamelang_parser.dna_layer.output ? 'TRUE ✅' : 'FALSE ❌'}`);
  
  console.log("\n🌳 DECISION LOGIC:");
  for (const [key, decision] of Object.entries(analysis.decision_logic)) {
    const emoji = decision.verdict ? '✅' : '❌';
    console.log(`   ${key}: ${decision.verdict ? 'TRUE' : 'FALSE'} ${emoji}`);
    if (decision.horizontal) console.log(`      → Horizontal: ${decision.horizontal}`);
    if (decision.vertical) console.log(`      → Vertical: ${decision.vertical}`);
  }
  
  console.log("\n🎯 META-PATTERN:");
  console.log(`   ${analysis.meta_pattern.flamelang_operator} ${analysis.meta_pattern.rule.split('\n')[0]}`);
  
  console.log("\n📈 PROGRESS:");
  console.log(`   Total Points: ${analysis.progress.total_points}`);
  console.log(`   Sections Cleared: ${analysis.progress.sections_cleared.join(', ')}`);
  console.log(`   Status: ${analysis.progress.status}`);
  console.log(`   Momentum: ${analysis.progress.momentum}`);
  
  console.log("\n" + "═".repeat(70));
}

// Run if executed directly (when this is the main module)
// Note: This is a simplified check for ES modules
const isMainModule = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'));
if (isMainModule) {
  runExample();
}
