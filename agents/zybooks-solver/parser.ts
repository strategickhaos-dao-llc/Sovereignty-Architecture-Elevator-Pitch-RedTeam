/**
 * zyBooks Parser - VESSEL MODE
 * Parses zyBooks content and returns answers in YAML
 * No explanations, just answers
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

interface Question {
  id: number;
  type: 'multiple_choice' | 'fill_in' | 'coding' | 'true_false' | 'short_answer';
  topic: string;
  difficulty: string;
  text: string;
}

interface Answer {
  question_id: number;
  answer: string;
  confidence: 'high' | 'medium' | 'low';
}

interface ParsedContent {
  metadata: {
    session_id: string;
    timestamp: string;
    source: string;
    mode: string;
    operator: string;
  };
  questions: Question[];
  answers: Answer[];
  patterns_logged: {
    path: string;
    files: string[];
    flamelang_ready: boolean;
  };
  status: {
    processed: boolean;
    answers_count: number;
    training_data_logged: boolean;
    next_action: string;
  };
}

/**
 * Parse zyBooks content and extract questions
 */
export function parseZyBooksContent(content: string): ParsedContent {
  const sessionId = `zybooks_${new Date().toISOString().replace(/[:.]/g, '_')}`;
  const timestamp = new Date().toISOString();
  
  // Extract questions from content
  const questions = extractQuestions(content);
  
  // Generate answers (in VESSEL MODE - direct answers only)
  const answers = generateAnswers(questions);
  
  // Log patterns for FlameLang training
  const patternFiles = logPatterns(sessionId, questions, answers);
  
  const result: ParsedContent = {
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
  
  return result;
}

/**
 * Extract questions from raw zyBooks content
 */
function extractQuestions(content: string): Question[] {
  const questions: Question[] = [];
  
  // Patterns to identify different question types
  const patterns = {
    multipleChoice: /(?:Question|Q)\s*(\d+)[:\.]?\s*(.*?)(?:A\.|a\.|Options:|Choices:)/gis,
    fillIn: /(?:Fill in|Complete|Enter)[:\s]+(.*?)$/gim,
    trueOrFalse: /(?:True or False|T\/F)[:\s]+(.*?)$/gim,
    coding: /(?:Write|Code|Implement|Function)[:\s]+(.*?)$/gim
  };
  
  // Parse multiple choice questions
  let match;
  let id = 1;
  
  // Split by common question separators
  const sections = content.split(/\n\s*\n/);
  
  for (const section of sections) {
    if (section.trim().length < 10) continue;
    
    // Detect question type based on content
    let type: Question['type'] = 'short_answer';
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
function extractTopic(text: string): string {
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
function estimateDifficulty(text: string): string {
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
function generateAnswers(questions: Question[]): Answer[] {
  return questions.map(q => ({
    question_id: q.id,
    answer: '[ANSWER_PLACEHOLDER - Parse from zyBooks content or generate via LLM]',
    confidence: 'high'
  }));
}

/**
 * Log patterns for FlameLang training
 */
function logPatterns(sessionId: string, questions: Question[], answers: Answer[]): string[] {
  const trainingDir = path.join(process.cwd(), 'training', 'zybooks');
  
  // Ensure directory exists
  if (!fs.existsSync(trainingDir)) {
    fs.mkdirSync(trainingDir, { recursive: true });
  }
  
  const files: string[] = [];
  
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
 * Convert parsed content to YAML
 */
export function toYAML(content: ParsedContent): string {
  return yaml.dump(content, {
    indent: 2,
    lineWidth: 100,
    noRefs: true
  });
}

/**
 * Main entry point
 */
export function processZyBooks(content: string): string {
  const parsed = parseZyBooksContent(content);
  return toYAML(parsed);
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage: tsx parser.ts <input-file>');
    console.log('   or: echo "content" | tsx parser.ts');
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
