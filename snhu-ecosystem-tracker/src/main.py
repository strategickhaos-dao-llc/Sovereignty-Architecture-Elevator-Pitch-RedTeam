#!/usr/bin/env python3
"""
SNHU Ecosystem Analyzer - Main Application

This application analyzes SNHU emails for ecosystem insights using the Grok API.
It can run as a web service or as a batch processor.
"""

import os
import sys
import logging
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from email_analyzer import EmailAnalyzer


# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health checks and basic API."""
    
    def do_GET(self):
        """Handle GET requests for health checks."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'snhu-analyzer',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/ready':
            # Check if Grok API key is configured
            api_key = os.getenv('GROK_API_KEY')
            if api_key:
                self.send_response(200)
                response = {'status': 'ready'}
            else:
                self.send_response(503)
                response = {'status': 'not ready', 'reason': 'GROK_API_KEY not configured'}
            
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Override to use logger instead of stderr."""
        logger.info(f"{self.client_address[0]} - {format % args}")


def run_server(port: int = 8080):
    """
    Run the HTTP server for health checks and API endpoints.
    
    Args:
        port: Port to listen on
    """
    logger.info(f"Starting SNHU Analyzer HTTP server on port {port}")
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.shutdown()


def run_batch_analysis(input_file: str, output_file: str = None):
    """
    Run batch analysis on email file.
    
    Args:
        input_file: Path to input email file (CSV or JSON)
        output_file: Path to output results file (optional)
    """
    logger.info(f"Starting batch analysis on {input_file}")
    
    try:
        # Initialize analyzer
        model = os.getenv('ANALYSIS_MODEL', 'grok-4-fast-reasoning')
        analyzer = EmailAnalyzer(model=model)
        
        # Determine file format
        file_ext = Path(input_file).suffix.lower()
        format = 'json' if file_ext == '.json' else 'csv'
        
        # Analyze emails
        results = analyzer.analyze_emails_batch(input_file, format=format)
        
        # Save results
        if output_file:
            output_path = Path(output_file)
        else:
            output_path = Path('/app/results') / f"analysis_results.{format}"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'csv':
            results.to_csv(output_path, index=False)
        else:
            results.to_json(output_path, orient='records', indent=2)
        
        logger.info(f"Analysis complete. Results saved to {output_path}")
        logger.info(f"Processed {len(results)} emails")
        
        # Print summary
        if 'error' in results.columns:
            errors = results['error'].notna().sum()
            logger.info(f"Successful: {len(results) - errors}, Errors: {errors}")
        
    except Exception as e:
        logger.error(f"Batch analysis failed: {str(e)}", exc_info=True)
        sys.exit(1)


def main():
    """Main entry point for the application."""
    logger.info("SNHU Ecosystem Analyzer starting...")
    
    # Check for required environment variables
    api_key = os.getenv('GROK_API_KEY')
    if not api_key:
        logger.warning("GROK_API_KEY not set. Some functionality will be limited.")
    
    # Determine mode of operation
    mode = os.getenv('RUN_MODE', 'server')
    
    if mode == 'batch':
        # Batch processing mode
        input_file = os.getenv('INPUT_FILE')
        if not input_file:
            logger.error("INPUT_FILE environment variable required for batch mode")
            sys.exit(1)
        
        output_file = os.getenv('OUTPUT_FILE')
        run_batch_analysis(input_file, output_file)
    else:
        # Server mode (default)
        port = int(os.getenv('PORT', 8080))
        run_server(port)


if __name__ == '__main__':
    main()
