/**
 * Example usage of the Survivorship Memory Engine
 * 
 * This file demonstrates how Nova and Lyra agents interact with Athena
 * to log attempts, learn from failures, and query historical context.
 */

import {
  SurvivorshipMemoryEngine,
  createLogEntry,
  Challenge,
  SurvivorshipLog,
} from './survivorship-memory';

// Create an instance of Athena's memory engine
const athena = new SurvivorshipMemoryEngine();

/**
 * Example 1: Nova agent attempts a challenge and fails
 */
function exampleNovaFailure() {
  console.log("\n=== Example 1: Nova Failure ===\n");
  
  // Define the challenge
  const challenge: Challenge = {
    id: "challenge-001",
    type: "api_integration",
    complexity: 7,
    requirements: ["REST", "authentication", "rate_limiting"],
    description: "Integrate with external API with OAuth2",
  };
  
  // Nova attempts and fails
  const failureLog = createLogEntry(
    "nova-001",
    "nova",
    challenge,
    "direct_oauth2_flow",
    "Attempting standard OAuth2 flow based on API documentation",
    {
      status: "failure",
      execution_time_seconds: 45,
      resources_consumed: {
        cpu_seconds: 12,
        memory_peak_mb: 256,
        api_calls_used: 5,
        wall_time_seconds: 45,
      },
      failure_mode: "authentication_failure",
      error_details: {
        error_type: "InvalidGrantError",
        error_message: "Token refresh failed: invalid_grant",
        failed_at_step: "token_refresh",
        recovery_attempted: true,
        recovery_successful: false,
      },
    },
    {
      what_worked: ["Initial authentication succeeded"],
      what_failed: ["Token refresh mechanism"],
      why_it_failed: [
        "API requires additional scope for refresh tokens",
        "Token expiry handling was incorrect",
      ],
      what_to_try_next: [
        "Request offline_access scope during initial auth",
        "Implement proactive token refresh before expiry",
        "Add better error handling for token refresh failures",
      ],
      generalizable_pattern: "For OAuth2 APIs, always request offline_access scope and implement proactive token refresh",
    },
    {
      system_load: 0.3,
      concurrent_agents: 2,
      time_of_day: new Date().toISOString(),
      recent_changes: [],
    }
  );
  
  // Log to Athena
  athena.logAttempt(failureLog);
  
  console.log(`Nova agent logged failure for challenge: ${challenge.id}`);
}

/**
 * Example 2: Another Nova agent succeeds using Athena's wisdom
 */
function exampleNovaSuccess() {
  console.log("\n=== Example 2: Nova Success (Learning Applied) ===\n");
  
  // Similar challenge
  const challenge: Challenge = {
    id: "challenge-002",
    type: "api_integration",
    complexity: 7,
    requirements: ["REST", "authentication", "rate_limiting"],
    description: "Integrate with another external API with OAuth2",
  };
  
  // Before attempting, Nova queries Athena
  const context = athena.provideContext(challenge);
  console.log("Athena's guidance:");
  console.log("- Approaches to avoid:", context.approaches_to_avoid);
  console.log("- Recommended approaches:", context.recommended_approaches);
  
  // Nova applies the lesson and succeeds
  const successLog = createLogEntry(
    "nova-002",
    "nova",
    challenge,
    "oauth2_with_offline_access",
    "Using OAuth2 with offline_access scope based on Athena's lesson from previous failure",
    {
      status: "success",
      execution_time_seconds: 30,
      resources_consumed: {
        cpu_seconds: 8,
        memory_peak_mb: 200,
        api_calls_used: 4,
        wall_time_seconds: 30,
      },
      quality_score: 9.5,
    },
    {
      what_worked: [
        "Requested offline_access scope during initial auth",
        "Implemented proactive token refresh",
        "Added comprehensive error handling",
      ],
      what_failed: [],
      why_it_failed: [],
      what_to_try_next: [],
      generalizable_pattern: "OAuth2 integration with offline_access scope and proactive refresh is the reliable pattern",
    },
    {
      system_load: 0.4,
      concurrent_agents: 3,
      time_of_day: new Date().toISOString(),
      recent_changes: [],
    }
  );
  
  athena.logAttempt(successLog);
  
  console.log(`Nova agent logged success for challenge: ${challenge.id}`);
  console.log("Athena learned: Success pattern reinforced for api_integration");
}

/**
 * Example 3: Multiple failures lead to pattern detection
 */
function examplePatternDetection() {
  console.log("\n=== Example 3: Pattern Detection from Multiple Failures ===\n");
  
  // Simulate 5 similar failures
  for (let i = 0; i < 5; i++) {
    const challenge: Challenge = {
      id: `challenge-timeout-${i}`,
      type: "database_query",
      complexity: 6,
      requirements: ["PostgreSQL", "complex_join", "large_dataset"],
      description: "Query large dataset with multiple joins",
    };
    
    const failureLog = createLogEntry(
      `nova-${100 + i}`,
      "nova",
      challenge,
      "direct_query",
      "Attempting direct query without optimization",
      {
        status: "failure",
        execution_time_seconds: 60,
        resources_consumed: {
          cpu_seconds: 60,
          memory_peak_mb: 1024,
          api_calls_used: 0,
          wall_time_seconds: 60,
        },
        failure_mode: "timeout",
        error_details: {
          error_type: "QueryTimeout",
          error_message: "Query exceeded 60 second timeout",
          failed_at_step: "query_execution",
          recovery_attempted: false,
        },
      },
      {
        what_worked: [],
        what_failed: ["Query execution"],
        why_it_failed: [
          "Dataset too large for direct query",
          "Missing index on join columns",
          "No query optimization applied",
        ],
        what_to_try_next: [
          "Add indexes on join columns",
          "Break query into smaller chunks",
          "Use materialized views",
          "Implement query result caching",
        ],
        generalizable_pattern: "Large dataset queries require indexing and optimization strategies",
      },
      {
        system_load: 0.8,
        concurrent_agents: 1,
        time_of_day: new Date().toISOString(),
        recent_changes: [],
      }
    );
    
    athena.logAttempt(failureLog);
  }
  
  // Give Athena time to process (in real system, this would be async)
  setTimeout(() => {
    console.log("\nAthena detected patterns:");
    const patterns = athena.getAllPatterns();
    patterns.forEach(pattern => {
      if (pattern.occurrences >= 3) {
        console.log(`- ${pattern.description} (confidence: ${pattern.confidence.toFixed(2)}, occurrences: ${pattern.occurrences})`);
      }
    });
  }, 100);
}

/**
 * Example 4: Lyra queries Athena before assigning a risky challenge
 */
function exampleRiskAssessment() {
  console.log("\n=== Example 4: Risk Assessment Before Assignment ===\n");
  
  const riskyChallenge: Challenge = {
    id: "challenge-risky-001",
    type: "database_query",
    complexity: 8,
    requirements: ["PostgreSQL", "complex_join", "large_dataset"],
    description: "Complex query on production database",
  };
  
  // Lyra queries Athena for risk assessment
  const riskAssessment = athena.predictFailureModes(riskyChallenge);
  
  console.log("Risk Assessment from Athena:");
  console.log(`Overall Risk Score: ${riskAssessment.overall_risk_score.toFixed(2)}/10`);
  console.log(`Confidence: ${(riskAssessment.confidence * 100).toFixed(0)}%`);
  console.log("\nPredicted Failure Modes:");
  
  riskAssessment.predicted_failure_modes.forEach(fm => {
    console.log(`- ${fm.mode}:`);
    console.log(`  Probability: ${(fm.probability * 100).toFixed(0)}%`);
    console.log(`  Severity: ${fm.severity}/10`);
    console.log(`  Mitigation: ${fm.mitigation_strategy}`);
  });
  
  // Based on risk, Lyra might:
  // - Assign to more experienced Nova
  // - Allocate more resources
  // - Add extra monitoring
  // - Require human approval before execution
}

/**
 * Example 5: Generate learning curriculum for new agent
 */
function exampleCurriculumGeneration() {
  console.log("\n=== Example 5: Learning Curriculum for New Agent ===\n");
  
  const curriculum = athena.generateCurriculum("nova");
  
  console.log("Top lessons for new Nova agent:");
  curriculum.forEach((lesson, index) => {
    console.log(`\n${index + 1}. ${lesson.title}`);
    console.log(`   Summary: ${lesson.summary}`);
    console.log(`   Confidence: ${(lesson.confidence * 100).toFixed(0)}%`);
    console.log(`   Evidence: ${lesson.evidence_count} supporting cases`);
    console.log(`   Actionable Advice:`);
    lesson.actionable_advice.forEach(advice => {
      console.log(`   - ${advice}`);
    });
  });
}

/**
 * Run all examples
 */
function runAllExamples() {
  console.log("╔════════════════════════════════════════════════════════╗");
  console.log("║  Athena Survivorship Memory Engine - Examples         ║");
  console.log("╚════════════════════════════════════════════════════════╝");
  
  exampleNovaFailure();
  
  setTimeout(() => {
    exampleNovaSuccess();
    
    setTimeout(() => {
      examplePatternDetection();
      
      setTimeout(() => {
        exampleRiskAssessment();
        
        setTimeout(() => {
          exampleCurriculumGeneration();
        }, 200);
      }, 200);
    }, 100);
  }, 100);
}

// Run examples if this file is executed directly
// Note: In ES modules, we use import.meta.url to check if file is main
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Check if this module is being run directly
if (process.argv[1] === __filename || process.argv[1].endsWith('example-usage.ts')) {
  runAllExamples();
}

export {
  exampleNovaFailure,
  exampleNovaSuccess,
  examplePatternDetection,
  exampleRiskAssessment,
  exampleCurriculumGeneration,
};
