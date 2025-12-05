#!/usr/bin/env python3
"""
Display final pipeline results with detailed statistics
"""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

def show_final_results():
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "📊 FINAL PIPELINE RESULTS" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    project_root = Path(__file__).parent
    all_jobs = []
    
    # 1. LinkedIn Results
    print("1️⃣  LinkedIn + The Muse Jobs:")
    print("─" * 70)
    linkedin_dir = project_root / "linkedin_collector" / "job_search_results"
    linkedin_jobs = []
    
    if linkedin_dir.exists():
        for file in sorted(linkedin_dir.glob("*.json")):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    # Handle both list and dict formats
                    if isinstance(data, dict) and 'jobs' in data:
                        jobs = data['jobs']
                    elif isinstance(data, list):
                        jobs = data
                    else:
                        jobs = []
                    linkedin_jobs.extend(jobs)
                    print(f"   ✅ {file.name}: {len(jobs)} jobs")
            except Exception as e:
                print(f"   ⚠️  Error reading {file.name}: {e}")
        
        # Count sources
        if linkedin_jobs:
            sources = Counter([j.get('source', '').split('/')[0] for j in linkedin_jobs])
            print(f"\n   📊 Total: {len(linkedin_jobs)} jobs")
            print(f"   📋 Sources breakdown:")
            for source, count in sources.items():
                print(f"      • {source}: {count} jobs")
            all_jobs.extend(linkedin_jobs)
    else:
        print("   ⚠️  No results found")
    
    # 2. GitHub Results
    print(f"\n2️⃣  GitHub Repository Jobs:")
    print("─" * 70)
    github_file = project_root / "data" / "jobs_output.json"
    github_jobs = []
    
    if github_file.exists():
        try:
            with open(github_file, 'r') as f:
                github_jobs = json.load(f)
                print(f"   ✅ jobs_output.json: {len(github_jobs)} jobs")
                
                # Show repo sources
                sources = Counter([j.get('source', 'Unknown') for j in github_jobs])
                print(f"   📋 Repository sources:")
                for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"      • {source}: {count} jobs")
                all_jobs.extend(github_jobs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    else:
        print("   ⚠️  No results found")
    
    # 3. Firecrawl Results
    print(f"\n3️⃣  Firecrawl Web Scraping Jobs:")
    print("─" * 70)
    firecrawl_jobs = []
    
    firecrawl_files = list((project_root / "data").glob("firecrawl_jobs_*.json"))
    if firecrawl_files:
        latest_file = max(firecrawl_files, key=lambda x: x.stat().st_mtime)
        try:
            with open(latest_file, 'r') as f:
                firecrawl_jobs = json.load(f)
                print(f"   ✅ {latest_file.name}: {len(firecrawl_jobs)} jobs")
                
                # Show sources
                sources = Counter([j.get('source', 'Unknown') for j in firecrawl_jobs])
                print(f"   📋 Web sources:")
                for source, count in sources.items():
                    print(f"      • {source}: {count} jobs")
                all_jobs.extend(firecrawl_jobs)
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    else:
        print("   ⚠️  No results found (may have been skipped)")
    
    # 4. Total Summary
    print(f"\n" + "=" * 70)
    print(f"📊 TOTAL JOBS COLLECTED: {len(all_jobs)}")
    print("=" * 70)
    
    if all_jobs:
        # Overall source breakdown
        print(f"\n🎯 Overall Source Breakdown:")
        all_sources = Counter()
        for job in all_jobs:
            source = job.get('source', 'Unknown')
            if '/' in source:
                source_type = source.split('/')[0]
            else:
                source_type = source
            all_sources[source_type] += 1
        
        for source, count in sorted(all_sources.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(all_jobs)) * 100
            print(f"   • {source:20s}: {count:4d} jobs ({percentage:5.1f}%)")
        
        # Show sample jobs
        print(f"\n📋 Sample Jobs (Top 5):")
        for i, job in enumerate(all_jobs[:5], 1):
            print(f"\n   {i}. {job.get('company', 'Unknown Company')}")
            print(f"      Position: {job.get('position', 'Unknown Position')}")
            print(f"      Location: {job.get('location', 'Unknown')}")
            print(f"      Source: {job.get('source', 'Unknown')}")
    
    # 5. Matched Jobs
    print(f"\n\n4️⃣  AI-Matched Jobs (Top 50):")
    print("─" * 70)
    matched_file = project_root / "matched_jobs" / "top_50_matches.json"
    
    if matched_file.exists():
        try:
            with open(matched_file, 'r') as f:
                matched_jobs = json.load(f)
                print(f"   ✅ top_50_matches.json: {len(matched_jobs)} jobs")
                
                if matched_jobs:
                    print(f"\n   🏆 Top 5 Best Matches:")
                    for i, job in enumerate(matched_jobs[:5], 1):
                        score = job.get('match_score', 'N/A')
                        print(f"\n   {i}. {job.get('company', 'Unknown')} - {job.get('position', 'Unknown')}")
                        print(f"      Match Score: {score}")
                        print(f"      Location: {job.get('location', 'Unknown')}")
                        reasoning = job.get('reasoning', '')
                        if reasoning:
                            print(f"      Why: {reasoning[:80]}...")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")
    else:
        print("   ⚠️  Matching not completed yet")
    
    print(f"\n" + "=" * 70)
    print(f"💾 All job files saved in:")
    print(f"   • LinkedIn: linkedin_collector/job_search_results/")
    print(f"   • GitHub: data/jobs_output.json")
    print(f"   • Firecrawl: data/firecrawl_jobs_*.json")
    print(f"   • Matched: matched_jobs/top_50_matches.json")
    print("=" * 70)

if __name__ == "__main__":
    show_final_results()
