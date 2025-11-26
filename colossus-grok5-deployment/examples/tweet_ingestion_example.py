#!/usr/bin/env python3
"""
Tweet Ingestion Example

Demonstrates how to use the X Provenance Pipeline to ingest tweets
with full provenance tracking.

Artifact #3558 - Colossus Grok-5 Deployment Suite
"""

import logging
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.x_provenance_pipeline import XProvenancePipeline


class MockDatabase:
    """Mock database for demonstration."""

    def __init__(self):
        self.batches = []

    def store_provenance_batch(self, records, root, ots_proof):
        self.batches.append({
            "records": records,
            "root": root,
            "ots_proof": ots_proof,
        })
        print(f"Stored batch: {len(records)} records, root={root[:16]}...")


def generate_sample_tweets():
    """Generate sample tweets for demonstration."""
    return [
        {"id": "1", "text": "Grok-5 training is going great! Excited for the future of AI."},
        {"id": "2", "text": "The weather is beautiful today. Perfect for a walk in the park."},
        {"id": "3", "text": "Just finished reading an amazing book about quantum computing."},
        {"id": "4", "text": "Love the new features in the latest software update!"},
        {"id": "5", "text": "Great discussion at the AI safety conference today."},
        {"id": "6", "text": "Working on some exciting machine learning projects."},
        {"id": "7", "text": "The new Colossus cluster is incredibly powerful."},
        {"id": "8", "text": "Happy to contribute to open source software development."},
        {"id": "9", "text": "Learning about distributed systems and consensus protocols."},
        {"id": "10", "text": "The team has made incredible progress this quarter."},
    ]


def main():
    """Run the tweet ingestion example."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger("tweet_ingestion")

    print("=" * 60)
    print("Tweet Ingestion Example - Colossus Grok-5")
    print("=" * 60)
    print()

    # Create mock database
    db = MockDatabase()

    # Create pipeline with small batch size for demo
    pipeline = XProvenancePipeline(
        db=db,
        batch_size=5,  # Small batch for demonstration
        logger=logger,
    )

    # Generate sample tweets
    tweets = generate_sample_tweets()
    print(f"Generated {len(tweets)} sample tweets")
    print()

    # Ingest tweets
    print("Ingesting tweets with provenance tracking...")
    print("-" * 60)

    stats = pipeline.ingest_stream(tweets)

    print()
    print("-" * 60)
    print("Ingestion Results:")
    print(f"  Total processed: {stats.total_processed}")
    print(f"  Accepted: {stats.accepted}")
    print(f"  Filtered (toxicity): {stats.filtered}")
    print(f"  Batches created: {stats.batches}")
    print()

    # Show stored batches
    print("Stored Batches:")
    for i, batch in enumerate(db.batches):
        print(f"  Batch {i + 1}:")
        print(f"    Records: {len(batch['records'])}")
        print(f"    Merkle Root: {batch['root'][:32]}...")
        print(f"    OTS Proof: {batch['ots_proof'][:32]}...")
    print()

    # Demonstrate verification
    print("Verifying batch provenance...")
    for batch in db.batches:
        is_valid = pipeline.verify_batch(batch["root"], batch["ots_proof"])
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"  Root {batch['root'][:16]}...: {status}")

    print()
    print("=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
