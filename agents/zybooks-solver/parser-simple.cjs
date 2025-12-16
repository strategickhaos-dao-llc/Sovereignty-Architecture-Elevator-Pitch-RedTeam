#!/usr/bin/env node
/**
 * zyBooks Parser - VESSEL MODE (Simple Version)
 * Parses zyBooks content and returns answers in YAML
 * No external dependencies - pure Node.js
 */

const fs = require('fs');
const path = require('path');

/**
 * Parse zyBooks content and extract questions
 */
function parseZyBooksContent(content) {
  const sessionId = `zybooks_${new Date().toISOString().replace(/[:.]/g, '_')}`;
  const timestamp = new Date().toISOString();
  
  // Extract questions from content
  const questions = extractQuestions(content);
  
  // Generate answers (in VESSEL MODE - direct answers only)
  const answers = generateAnswers(questions);
  
  // Log patterns for FlameLang training
  const patternFiles = logPatterns(sessionId, questions, answers);
  
  return {
    metadata: {
      session_id: sessionId,
      timestamp: timestamp,
      source: 'zyBooks',
      mode: 'VESSEL_MODE',
      operator: 'Dom'
    },
    questions: questions,
    answers: answers,
    patterns_logged: {
      path: 'training/zybooks/',
      files: patternFiles,
      flamelang_ready: true
    },
    status: {
      processed: true,
      answers_count: answers.length,
      training_data_logged: true,
      next_action: 'Send next section'
    }
  };
}

/**
 * Extract questions from raw zyBooks content
 */
function extractQuestions(content) {
  const questions = [];
  let id = 1;
  
  // Split by common question separators
  const sections = content.split(/\n\s*\n/);
  
  for (const section of sections) {
    if (section.trim().length < 10) continue;
    
    // Detect question type based on content
    let type = 'short_answer';
    if (/(?:A\.|a\.).*(?:B\.|b\.).*(?:C\.|c\.)/is.test(section)) {
      type = 'multiple_choice';
    } else if (/true|false/i.test(section) && section.length < 200) {
      type = 'true_false';
    } else if (/write|code|implement|function|class|method/i.test(section)) {
      type = 'coding';
    } else if (/fill in|complete|enter/i.test(section)) {
      type = 'fill_in';
    }
    
    questions.push({
      id: id++,
      type: type,
      topic: extractTopic(section),
      difficulty: estimateDifficulty(section),
      text: section.trim().substring(0, 500) // Truncate for brevity
    });
  }
  
  return questions;
}

/**
 * Extract topic from question text
 */
function extractTopic(text) {
  // Common CS/Cyber topics
  const topics = [
    'algorithms', 'data structures', 'networking', 'security', 
    'databases', 'operating systems', 'programming', 'web development',
    'python', 'java', 'javascript', 'c++', 'sql'
  ];
  
  const lowerText = text.toLowerCase();
  for (const topic of topics) {
    if (lowerText.includes(topic)) {
      return topic;
    }
  }
  
  return 'general';
}

/**
 * Estimate difficulty based on content
 */
function estimateDifficulty(text) {
  const length = text.length;
  const complexityMarkers = ['algorithm', 'implement', 'design', 'optimize', 'analyze'];
  
  let complexity = 0;
  for (const marker of complexityMarkers) {
    if (text.toLowerCase().includes(marker)) complexity++;
  }
  
  if (length > 500 || complexity >= 2) return 'hard';
  if (length > 200 || complexity >= 1) return 'medium';
  return 'easy';
}

/**
 * Generate answers for questions (VESSEL MODE - answers only)
 */
function generateAnswers(questions) {
  return questions.map(q => ({
    question_id: q.id,
    answer: '[ANSWER_PLACEHOLDER - Parse from zyBooks content or generate via LLM]',
    confidence: 'high'
  }));
}

/**
 * Log patterns for FlameLang training
 */
function logPatterns(sessionId, questions, answers) {
  const trainingDir = path.join(process.cwd(), 'training', 'zybooks');
  
  // Ensure directory exists
  if (!fs.existsSync(trainingDir)) {
    fs.mkdirSync(trainingDir, { recursive: true });
  }
  
  const files = [];
  
  // Log question structures
  const structuresFile = `${sessionId}_structures.json`;
  fs.writeFileSync(
    path.join(trainingDir, structuresFile),
    JSON.stringify({ questions }, null, 2)
  );
  files.push(structuresFile);
  
  // Log answer patterns
  const patternsFile = `${sessionId}_patterns.json`;
  fs.writeFileSync(
    path.join(trainingDir, patternsFile),
    JSON.stringify({ answers, metadata: { session_id: sessionId } }, null, 2)
  );
  files.push(patternsFile);
  
  return files;
}

/**
 * Convert object to YAML (simple implementation)
 */
function toYAML(obj, indent = 0) {
  let yaml = '';
  const spaces = '  '.repeat(indent);
  
  for (const [key, value] of Object.entries(obj)) {
    if (value === null || value === undefined) {
      yaml += `${spaces}${key}: null\n`;
    } else if (typeof value === 'object' && !Array.isArray(value)) {
      yaml += `${spaces}${key}:\n`;
      yaml += toYAML(value, indent + 1);
    } else if (Array.isArray(value)) {
      yaml += `${spaces}${key}:\n`;
      value.forEach(item => {
        if (typeof item === 'object') {
          yaml += `${spaces}  -\n`;
          yaml += toYAML(item, indent + 2).replace(/^  /, '    ');
        } else {
          yaml += `${spaces}  - ${item}\n`;
        }
      });
    } else if (typeof value === 'string') {
      yaml += `${spaces}${key}: "${value}"\n`;
    } else {
      yaml += `${spaces}${key}: ${value}\n`;
    }
  }
  
  return yaml;
}

/**
 * Main processing function
 */
function processZyBooks(content) {
  const parsed = parseZyBooksContent(content);
  return toYAML(parsed);
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage: node parser-simple.js <input-file>');
    console.log('   or: echo "content" | node parser-simple.js -');
    process.exit(1);
  }
  
  let content = '';
  
  if (args[0] === '-') {
    // Read from stdin
    content = fs.readFileSync(0, 'utf-8');
  } else {
    // Read from file
    content = fs.readFileSync(args[0], 'utf-8');
  }
  
  const result = processZyBooks(content);
  console.log(result);
}

module.exports = { processZyBooks, parseZyBooksContent };
