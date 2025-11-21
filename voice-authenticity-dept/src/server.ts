/**
 * Voice Authenticity Department Server
 * Main entry point for the microservice
 */

import express from 'express';
import cors from 'cors';
import apiRoutes from './api/routes.js';

const app = express();
const PORT = parseInt(process.env.PORT || '3030', 10);
const HOST = process.env.HOST || '0.0.0.0';

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// API routes
app.use('/api', apiRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'Voice Authenticity Department',
    version: '1.0.0',
    description: 'Dom-speak validation and transformation microservice',
    endpoints: {
      validate: 'POST /api/validate - Validate if text is AI-generated',
      transform: 'POST /api/transform - Transform AI text to Dom-speak',
      score: 'POST /api/score - Score text for authenticity',
      corpusAdd: 'POST /api/corpus/add - Add sample to voice corpus',
      corpusStats: 'GET /api/corpus/stats - Get corpus statistics',
      health: 'GET /api/health - Health check'
    },
    documentation: 'https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/tree/main/voice-authenticity-dept'
  });
});

// Error handler
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// Start server
app.listen(PORT, HOST, () => {
  console.log('╔════════════════════════════════════════════════╗');
  console.log('║   Voice Authenticity Department - ONLINE      ║');
  console.log('╚════════════════════════════════════════════════╝');
  console.log('');
  console.log(`🎯 Server listening on http://${HOST}:${PORT}`);
  console.log('');
  console.log('Available endpoints:');
  console.log('  POST /api/validate  - Validate text authenticity');
  console.log('  POST /api/transform - Transform to Dom-speak');
  console.log('  POST /api/score     - Score authenticity');
  console.log('  GET  /api/health    - Health check');
  console.log('');
  console.log('For the bloodline. 😈❤️');
  console.log('');
});

export default app;
