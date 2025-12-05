#!/usr/bin/env python3
"""
Quick test of Firecrawl scraper
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# Import after path is set
from API_collector.firecrawl_scraper import FirecrawlJobScraper

def test_scraper():
    """Test if firecrawl scraper works"""
    print("🔥 Testing Firecrawl Job Scraper...")
    print("=" * 70)
    
    try:
        # Initialize scraper
        scraper = FirecrawlJobScraper()
        print("✅ Scraper initialized successfully")
        
        # Test with minimal jobs
        print("\n📊 Testing JobRight.ai scraping (max 5 jobs)...")
        jobs = scraper.scrape_jobright(
            search_query="machine learning",
            max_jobs=5
        )
        
        print(f"\n{'='*70}")
        print(f"✅ SUCCESS: Retrieved {len(jobs)} jobs from JobRight.ai")
        print(f"{'='*70}")
        
        if jobs:
            print("\n📋 Sample Jobs:")
            for i, job in enumerate(jobs[:3], 1):
                print(f"\n{i}. {job.company}")
                print(f"   Position: {job.position}")
                print(f"   Location: {job.location}")
                print(f"   Source: {job.source}")
                print(f"   URL: {job.apply_link[:60]}...")
        else:
            print("\n⚠️  No jobs retrieved - API might be rate limited or site structure changed")
        
        return len(jobs) > 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1)
