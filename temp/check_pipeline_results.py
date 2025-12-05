#!/usr/bin/env python3
"""
Check pipeline results and show final job collection statistics
"""

import json
from pathlib import Path
from collections import Counter

def check_results():
    print("=" * 70)
    print("📊 PIPELINE RESULTS CHECKER")
    print("=" * 70)
    
    project_root = Path(__file__).parent
    
    # Check LinkedIn results
    print("\n1️⃣  LinkedIn Collector Results:")
    linkedin_dir = project_root / "linkedin_collector" / "job_search_results"
    if linkedin_dir.exists():
        json_files = list(linkedin_dir.glob("*.json"))
        if json_files:
            total_linkedin = 0
            for file in json_files:
                try:
                    with open(file, 'r') as f:
                        jobs = json.load(f)
                        count = len(jobs)
                        total_linkedin += count
                        print(f"   ✅ {file.name}: {count} jobs")
                except:
                    pass
            print(f"   📊 Total LinkedIn jobs: {total_linkedin}")
        else:
            print("   ⚠️  No LinkedIn results yet")
    else:
        print("   ⚠️  LinkedIn results directory not found")
    
    # Check GitHub results
    print("\n2️⃣  GitHub Collector Results:")
    github_output = project_root / "data" / "jobs_output.json"
    if github_output.exists():
        try:
            with open(github_output, 'r') as f:
                jobs = json.load(f)
                print(f"   ✅ jobs_output.json: {len(jobs)} jobs")
                
                # Show sources
                sources = Counter([job.get('source', 'unknown') for job in jobs])
                print(f"   📋 Sources: {dict(sources)}")
        except Exception as e:
            print(f"   ⚠️  Error reading file: {e}")
    else:
        print("   ⚠️  No GitHub results yet (data/jobs_output.json)")
    
    # Check Firecrawl results
    print("\n3️⃣  Firecrawl Collector Results:")
    firecrawl_dir = project_root / "data"
    if firecrawl_dir.exists():
        firecrawl_files = list(firecrawl_dir.glob("firecrawl_jobs_*.json"))
        if firecrawl_files:
            for file in sorted(firecrawl_files, key=lambda x: x.stat().st_mtime, reverse=True)[:1]:
                try:
                    with open(file, 'r') as f:
                        jobs = json.load(f)
                        print(f"   ✅ {file.name}: {len(jobs)} jobs")
                        
                        # Show sources
                        sources = Counter([job.get('source', 'unknown') for job in jobs])
                        print(f"   📋 Sources: {dict(sources)}")
                except Exception as e:
                    print(f"   ⚠️  Error reading file: {e}")
        else:
            print("   ⚠️  No Firecrawl results yet")
    
    # Check matched jobs
    print("\n4️⃣  Matched Jobs Results:")
    matched_file = project_root / "matched_jobs" / "top_50_matches.json"
    if matched_file.exists():
        try:
            with open(matched_file, 'r') as f:
                jobs = json.load(f)
                print(f"   ✅ top_50_matches.json: {len(jobs)} jobs")
                
                if jobs:
                    print(f"\n   📋 Top 3 Matches:")
                    for i, job in enumerate(jobs[:3], 1):
                        print(f"   {i}. {job.get('company', 'Unknown')} - {job.get('position', 'Unknown')}")
                        print(f"      Match Score: {job.get('match_score', 'N/A')}")
        except Exception as e:
            print(f"   ⚠️  Error reading file: {e}")
    else:
        print("   ⚠️  No matched jobs yet (pipeline still running)")
    
    print("\n" + "=" * 70)
    print("💡 To see real-time progress, check the terminal running run_pipeline.py")
    print("=" * 70)

if __name__ == "__main__":
    check_results()
