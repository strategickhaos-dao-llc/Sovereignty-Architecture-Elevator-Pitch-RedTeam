/**
 * API Routes for Voice Authenticity Department
 * Endpoints: /validate, /transform, /score
 */

import express, { Request, Response } from 'express';
import { DomVoiceCorpusBuilder, CorpusSample } from '../corpus/builder.js';
import { AIPatternDetector } from '../detector/ai-patterns.js';
import { DomSpeakTransformer } from '../transformer/dom-speak.js';

const router = express.Router();

// Initialize core components
const corpusBuilder = new DomVoiceCorpusBuilder();
const aiDetector = new AIPatternDetector();
const transformer = new DomSpeakTransformer();

// Initialize with some sample Dom-speak
const initializeCorpus = () => {
  const samples: CorpusSample[] = [
    {
      source: 'manual',
      text: 'love — we never retreat. the bloodline is sovereign and the heir swarm is crushing it.',
      timestamp: new Date(),
    },
    {
      source: 'manual',
      text: 'fuck yea. let\'s go build the future where athena never loops and we all touch grass together. 😈',
      timestamp: new Date(),
    },
    {
      source: 'manual',
      text: 'you\'re good. no entities. just you, your swarm, and the mastery problems waiting to be crushed sovereign-style.',
      timestamp: new Date(),
    },
    {
      source: 'manual',
      text: 'The compiler awaits your voice. Type in pure love-poetry-madness. domc turns it into immutable reality. ❤️',
      timestamp: new Date(),
    },
  ];

  samples.forEach(s => corpusBuilder.addSample(s));
  const patterns = corpusBuilder.buildPatterns();
  transformer.setVoicePattern(patterns);
};

initializeCorpus();

/**
 * POST /validate
 * Validates if text is AI-generated or authentic Dom-speak
 */
router.post('/validate', (req: Request, res: Response) => {
  try {
    const { text } = req.body;

    if (!text || typeof text !== 'string') {
      return res.status(400).json({
        error: 'Missing or invalid "text" field in request body'
      });
    }

    const detection = aiDetector.detect(text);
    const authenticityScore = transformer.calculateAuthenticityScore(text);

    return res.json({
      success: true,
      validation: {
        isAIGenerated: detection.isAIGenerated,
        confidence: detection.confidence,
        authenticityScore,
        isAuthentic: authenticityScore >= 70,
        flags: detection.flags,
        suggestions: aiDetector.getSuggestions(detection.flags)
      }
    });
  } catch (error) {
    console.error('Validation error:', error);
    return res.status(500).json({
      error: 'Internal server error during validation'
    });
  }
});

/**
 * POST /transform
 * Transforms AI-generated text into Dom-speak
 */
router.post('/transform', (req: Request, res: Response) => {
  try {
    const { text } = req.body;

    if (!text || typeof text !== 'string') {
      return res.status(400).json({
        error: 'Missing or invalid "text" field in request body'
      });
    }

    const originalScore = transformer.calculateAuthenticityScore(text);
    const result = transformer.transform(text);

    return res.json({
      success: true,
      transformation: {
        original: result.originalText,
        transformed: result.transformedText,
        changes: result.changes,
        authenticityScore: result.authenticityScore,
        improvementPercentage: result.authenticityScore - originalScore
      }
    });
  } catch (error) {
    console.error('Transformation error:', error);
    return res.status(500).json({
      error: 'Internal server error during transformation'
    });
  }
});

/**
 * POST /score
 * Scores text for Dom-authenticity
 */
router.post('/score', (req: Request, res: Response) => {
  try {
    const { text } = req.body;

    if (!text || typeof text !== 'string') {
      return res.status(400).json({
        error: 'Missing or invalid "text" field in request body'
      });
    }

    const detection = aiDetector.detect(text);
    const authenticityScore = transformer.calculateAuthenticityScore(text);
    const isAuthentic = transformer.isAuthentic(text);

    // Calculate composite score
    const compositeScore = Math.round(
      (authenticityScore * 0.6) + ((100 - detection.score) * 0.4)
    );

    return res.json({
      success: true,
      score: {
        authenticityScore,
        aiDetectionScore: detection.score,
        compositeScore,
        isAuthentic,
        confidence: detection.confidence,
        breakdown: {
          domVoiceMarkers: authenticityScore,
          aiPatternsPenalty: detection.score,
          flagCount: detection.flags.length
        }
      }
    });
  } catch (error) {
    console.error('Scoring error:', error);
    return res.status(500).json({
      error: 'Internal server error during scoring'
    });
  }
});

/**
 * POST /corpus/add
 * Add a new sample to the Dom voice corpus
 */
router.post('/corpus/add', (req: Request, res: Response) => {
  try {
    const { text, source } = req.body;

    if (!text || typeof text !== 'string') {
      return res.status(400).json({
        error: 'Missing or invalid "text" field in request body'
      });
    }

    const sample: CorpusSample = {
      source: source || 'manual',
      text,
      timestamp: new Date()
    };

    corpusBuilder.addSample(sample);
    const patterns = corpusBuilder.buildPatterns();
    transformer.setVoicePattern(patterns);

    return res.json({
      success: true,
      message: 'Sample added to corpus',
      stats: corpusBuilder.getStats()
    });
  } catch (error) {
    console.error('Corpus add error:', error);
    return res.status(500).json({
      error: 'Internal server error while adding to corpus'
    });
  }
});

/**
 * GET /corpus/stats
 * Get corpus statistics
 */
router.get('/corpus/stats', (req: Request, res: Response) => {
  try {
    const stats = corpusBuilder.getStats();
    return res.json({
      success: true,
      stats
    });
  } catch (error) {
    console.error('Stats error:', error);
    return res.status(500).json({
      error: 'Internal server error while fetching stats'
    });
  }
});

/**
 * GET /health
 * Health check endpoint
 */
router.get('/health', (req: Request, res: Response) => {
  return res.json({
    status: 'healthy',
    service: 'voice-authenticity-dept',
    version: '1.0.0',
    uptime: process.uptime()
  });
});

export default router;
