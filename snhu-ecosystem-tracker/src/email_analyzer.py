import os
from openai import OpenAI
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EmailAnalyzer:
    """Analyzes SNHU emails using Grok API for ecosystem insights."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "grok-4-fast-reasoning"):
        """
        Initialize the EmailAnalyzer with Grok API credentials.
        
        Args:
            api_key: Grok API key (defaults to GROK_API_KEY env var)
            model: Model to use for analysis
        """
        self.api_key = api_key or os.getenv('GROK_API_KEY')
        if not self.api_key:
            raise ValueError("GROK_API_KEY must be provided or set as environment variable")
        
        self.model = model
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )
        logger.info(f"Initialized EmailAnalyzer with model: {model}")
    
    def analyze_email(self, subject: str, body: str, email_id: str = None) -> Dict:
        """
        Analyze a single email for ecosystem insights.
        
        Args:
            subject: Email subject line
            body: Email body content
            email_id: Optional identifier for the email
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = f"""Analyze this SNHU email for ecosystem insights:

Subject: {subject}
Body: {body}

Extract the following:
1. Key topics (e.g., credentials, SDN, skills, milestones)
2. Sentiment (positive, neutral, negative)
3. Stepping stones or milestones mentioned
4. Skills or competencies referenced
5. Any actionable items or deadlines

Provide a structured JSON response."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            insights = response.choices[0].message.content
            
            return {
                'email_id': email_id or 'unknown',
                'subject': subject,
                'insights': insights,
                'model': self.model,
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing email {email_id}: {str(e)}")
            return {
                'email_id': email_id or 'unknown',
                'subject': subject,
                'error': str(e)
            }
    
    def analyze_emails_batch(self, email_file: str, format: str = 'csv') -> pd.DataFrame:
        """
        Analyze a batch of emails from a file.
        
        Args:
            email_file: Path to file containing emails
            format: File format ('csv' or 'json')
            
        Returns:
            DataFrame with analysis results
        """
        logger.info(f"Loading emails from {email_file}")
        
        if format == 'csv':
            df = pd.read_csv(email_file)
        elif format == 'json':
            df = pd.read_json(email_file)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if 'subject' not in df.columns or 'body' not in df.columns:
            raise ValueError("Email file must contain 'subject' and 'body' columns")
        
        results = []
        total = len(df)
        
        for idx, row in df.iterrows():
            logger.info(f"Analyzing email {idx + 1}/{total}")
            
            email_id = row.get('id', f"email_{idx}")
            result = self.analyze_email(
                subject=row['subject'],
                body=row['body'],
                email_id=str(email_id)
            )
            results.append(result)
        
        logger.info(f"Completed analysis of {total} emails")
        return pd.DataFrame(results)
    
    def extract_topics(self, insights_text: str) -> List[str]:
        """
        Extract key topics from analysis insights.
        
        Args:
            insights_text: The insights text from analysis
            
        Returns:
            List of identified topics
        """
        keywords = ['credential', 'stackable', 'SDN', 'skills', 'milestone', 
                   'ecosystem', 'course', 'learning', 'competency']
        
        topics = [kw for kw in keywords if kw.lower() in insights_text.lower()]
        return topics
