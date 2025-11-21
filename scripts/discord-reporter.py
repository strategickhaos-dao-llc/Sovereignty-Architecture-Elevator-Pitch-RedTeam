#!/usr/bin/env python3
"""
Discord Reporter
Posts progress updates to Discord webhook
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List
import requests

# Configuration
RESULTS_DIR = Path("/app/results")
ANALYSIS_DIR = Path("/app/analysis")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
REPORT_INTERVAL = int(os.getenv("REPORT_INTERVAL", "3600"))  # 1 hour default


def send_discord_message(content: str, embeds: List[Dict] = None):
    """Send message to Discord webhook"""
    if not DISCORD_WEBHOOK_URL:
        print("No Discord webhook URL configured")
        return False
    
    payload = {
        "content": content,
        "username": "SME Resource Bot"
    }
    
    if embeds:
        payload["embeds"] = embeds
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send Discord message: {e}")
        return False


def create_summary_embed() -> Dict:
    """Create summary embed from latest results"""
    
    # Find latest files
    result_files = sorted(RESULTS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    analysis_files = sorted(ANALYSIS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    fields = []
    
    # Evolution matches
    if result_files:
        try:
            with open(result_files[0], 'r') as f:
                data = json.load(f)
            
            processed = data.get("processed_items", 0)
            total_matches = sum(m.get("matched_count", 0) for m in data.get("matches", []))
            
            fields.append({
                "name": "🎯 Evolution Matching",
                "value": f"Processed: {processed} items\nTotal matches: {total_matches}",
                "inline": True
            })
        except:
            pass
    
    # Analysis results
    if analysis_files:
        try:
            with open(analysis_files[0], 'r') as f:
                data = json.load(f)
            
            topic = data.get("topic", "Unknown")
            analyzed = data.get("analyzed_count", 0)
            
            fields.append({
                "name": "🔍 Latest Analysis",
                "value": f"Topic: {topic}\nResources: {analyzed}",
                "inline": True
            })
        except:
            pass
    
    # Build embed
    embed = {
        "title": "📊 SME Resources Status Report",
        "description": "Latest processing status for sovereign infrastructure knowledge base",
        "color": 3447003,  # Blue
        "fields": fields,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "footer": {
            "text": "Sovereignty Architecture SME Bot"
        }
    }
    
    return embed


def report_startup():
    """Send startup notification"""
    content = "🚀 **SME Resource Bot Started**\n\nMonitoring knowledge base updates and analysis results."
    send_discord_message(content)


def report_periodic():
    """Send periodic status report"""
    embed = create_summary_embed()
    send_discord_message("📊 Periodic Status Report", embeds=[embed])


def main():
    print("=" * 80)
    print("Discord Reporter")
    print("=" * 80)
    print(f"Results directory: {RESULTS_DIR}")
    print(f"Analysis directory: {ANALYSIS_DIR}")
    print(f"Report interval: {REPORT_INTERVAL}s")
    print(f"Webhook configured: {'Yes' if DISCORD_WEBHOOK_URL else 'No'}")
    print()
    
    if not DISCORD_WEBHOOK_URL:
        print("⚠️  DISCORD_WEBHOOK_URL not set. Reporter will not send messages.")
        print("Set DISCORD_WEBHOOK_URL environment variable to enable Discord notifications.")
        # Still run but don't send messages
    
    # Send startup notification
    report_startup()
    
    # Periodic reporting loop
    last_report = time.time()
    
    print("Reporter running. Press Ctrl+C to stop.")
    print()
    
    try:
        while True:
            current_time = time.time()
            
            # Check if it's time for a report
            if current_time - last_report >= REPORT_INTERVAL:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sending periodic report...")
                report_periodic()
                last_report = current_time
            
            # Sleep for a bit
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n\nShutting down reporter...")
        send_discord_message("👋 SME Resource Bot shutting down.")


if __name__ == "__main__":
    main()
