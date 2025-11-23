import os
import sys
import pandas as pd
from openai import OpenAI

# Validate API key
api_key = os.getenv("GROK_API_KEY")
if not api_key:
    print("Error: GROK_API_KEY environment variable is not set")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

def analyze_email(subject, body):
    prompt = f"""
    You are an expert SNHU ecosystem analyst.
    Email from SNHU (@snhu.edu):
    Subject: {subject}
    Body: {body}

    Extract:
    - Main topic (credential, course, career services, SDN, etc.)
    - Sentiment (positive/neutral/negative)
    - Any "stepping stone" or milestone mentioned
    - Action items for the student
    Keep response concise, max 5 lines.
    """
    try:
        resp = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        if resp.choices and len(resp.choices) > 0:
            return resp.choices[0].message.content
        else:
            return "Error: No response from API"
    except Exception as e:
        return f"Error analyzing email: {str(e)}"

# Simulate your exported SNHU emails – replace with real CSV or IMAP later
emails = [
    {"subject": "Your new credential is ready!", "body": "Congrats on completing the Google IT Support certificate..."},
    {"subject": "SDN Project Team Invitation", "body": "We'd love to have you on the Spring 2026 SDN capstone..."},
]

for i, email in enumerate(emails, 1):
    insight = analyze_email(email["subject"], email["body"])
    print(f"\nEmail {i} Insight:\n{insight}")
