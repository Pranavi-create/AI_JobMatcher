#!/usr/bin/env python3
"""
Firecrawl job collection wrapper for pipeline integration
Safely collects jobs from JobRight.ai, Simplify, and Wellfound
Falls back gracefully if API fails or has no credits
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from API_collector.firecrawl_scraper import FirecrawlJobScraper
from models.job import Job

# Load environment
env_file = parent_dir / '.env'
load_dotenv(env_file)


def collect_firecrawl_jobs(
    search_queries: list = None,
    max_jobs_per_query: int = 20,
    output_dir: str = None
) -> list:
    """
    Collect jobs using Firecrawl scraper
    
    Args:
        search_queries: List of search keywords (default: load from search_keywords.txt)
        max_jobs_per_query: Max jobs per query per site
        output_dir: Where to save results (default: data/)
        
    Returns:
        List of Job objects collected
    """
    print("\n" + "=" * 70)
    print("🔥 COLLECTING JOBS VIA FIRECRAWL")
    print("=" * 70)
    
    # Check for API key
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("⚠️  FIRECRAWL_API_KEY not found in .env")
        print("   Skipping Firecrawl collection (LinkedIn and GitHub will still work)")
        return []
    
    try:
        # Initialize scraper
        scraper = FirecrawlJobScraper(api_key)
        print("✅ Firecrawl scraper initialized")
        
        # Load search queries if not provided
        if search_queries is None:
            keywords_file = parent_dir / "search_keywords.txt"
            if keywords_file.exists():
                search_queries = []
                with open(keywords_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Extract just the keyword part (before |)
                            keyword = line.split('|')[0].strip() if '|' in line else line
                            search_queries.append(keyword)
                print(f"✅ Loaded {len(search_queries)} search queries from search_keywords.txt")
            else:
                search_queries = ["machine learning", "AI engineer", "data scientist"]
                print(f"⚠️  Using default search queries")
        
        # Scrape all sources
        print(f"\n📊 Scraping {len(search_queries)} queries across 3 sources...")
        print(f"   Max jobs per query: {max_jobs_per_query}")
        
        all_jobs = scraper.scrape_all(
            search_queries=search_queries,
            max_jobs_per_query=max_jobs_per_query
        )
        
        print(f"\n{'='*70}")
        print(f"✅ Firecrawl collection complete: {len(all_jobs)} jobs")
        print(f"{'='*70}")
        
        # Save to file if output_dir specified
        if output_dir and all_jobs:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_path / f"firecrawl_jobs_{timestamp}.json"
            
            jobs_data = [job.model_dump() for job in all_jobs]
            with open(output_file, 'w') as f:
                json.dump(jobs_data, f, indent=2, default=str)
            
            print(f"💾 Saved to: {output_file}")
        
        return all_jobs
        
    except Exception as e:
        error_msg = str(e)
        
        # Handle specific errors gracefully
        if "Payment Required" in error_msg or "Insufficient credits" in error_msg:
            print(f"\n⚠️  Firecrawl API: Insufficient credits")
            print(f"   Skipping Firecrawl collection (other collectors will still work)")
            print(f"   To add credits: https://firecrawl.dev/pricing")
        elif "API key" in error_msg:
            print(f"\n⚠️  Firecrawl API key issue: {error_msg}")
            print(f"   Skipping Firecrawl collection")
        else:
            print(f"\n⚠️  Firecrawl error: {error_msg}")
            print(f"   Skipping Firecrawl collection (other collectors will still work)")
        
        return []


if __name__ == "__main__":
    # Test run
    print("Testing Firecrawl job collection...")
    
    # Use small limits for testing
    jobs = collect_firecrawl_jobs(
        search_queries=["machine learning"],
        max_jobs_per_query=5,
        output_dir="data"
    )
    
    if jobs:
        print(f"\n✅ Test successful: {len(jobs)} jobs collected")
        print("\n📋 Sample jobs:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job.company}")
            print(f"   {job.position}")
            print(f"   {job.location}")
    else:
        print("\n⚠️  No jobs collected (may need API credits)")
