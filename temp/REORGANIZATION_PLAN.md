# Project Reorganization Plan

## Current Issues:
1. job_matcher.py in root AND linkedin_collector/ (duplicate)
2. Inconsistent naming: github_fetcher.py but search_and_save.py (should be linkedin_fetcher.py)
3. Data scattered: job_search_results/, matched_jobs/, data/ in multiple places
4. Multiple MCP files: job_matcher_mcp_complete.py, job_matcher_mcp_server.py, job_matcher_mcp_stdio.py
5. Duplicate requirements.txt and README.md files

## Proposed New Structure:

```
Project/
├── collectors/                    # All data collection modules
│   ├── __init__.py
│   ├── linkedin_fetcher.py       # Renamed from search_and_save.py
│   ├── github_fetcher.py         # Moved from github_collector/
│   ├── themuse_fetcher.py        # Renamed from job_searcher.py
│   ├── firecrawl_fetcher.py      # Renamed from firecrawl_scraper.py
│   └── github_discovery.py       # Keep for dynamic repo discovery
│
├── data/                          # Central data storage
│   └── runs/                      # Timestamped run folders
│       └── run_YYYYMMDD_HHMMSS/
│           ├── linkedin_jobs.json
│           ├── github_jobs.json
│           ├── themuse_jobs.json
│           ├── firecrawl_jobs.json
│           ├── all_jobs.json      # Aggregated
│           └── matched_jobs.json  # Top 50 matches
│
├── matchers/                      # Matching logic
│   ├── __init__.py
│   ├── gemini_matcher.py         # Renamed from job_matcher.py
│   └── keyword_matcher.py        # Fallback matcher
│
├── mcp/                           # MCP server integration
│   ├── __init__.py
│   └── job_search_mcp_server.py  # Single MCP server file
│
├── models/                        # Data models
│   ├── __init__.py
│   └── job.py
│
├── utils/                         # Utilities
│   ├── __init__.py
│   ├── email_sender.py           # Renamed from send_email_smtp.py
│   └── resume_parser.py          # Extract from job_matcher.py
│
├── Resume/                        # Resume storage
│
├── pipeline_orchestrator.py      # Renamed from run_pipeline.py
├── mcp-server-config.json
├── requirements.txt              # Single requirements file
├── .env
├── .gitignore
├── README.md
├── PROJECT_REPORT.md
└── activate_jobly.sh
```

## Files to Remove (duplicates/deprecated):
- linkedin_collector/ (entire folder - merge into collectors/)
- github_collector/ (entire folder - merge into collectors/)
- API_collector/ (entire folder - merge into collectors/)
- matched_jobs/ (consolidate into data/runs/)
- job_matcher_mcp_server.py (keep only job_matcher_mcp_complete.py → rename to mcp/)
- job_matcher_mcp_stdio.py (deprecated)
- check_pipeline_results.py (utility script, can remove)
- show_final_results.py (utility script, can remove)
- test_integration.py (utility script, can remove)

## Renaming Convention:
- *_fetcher.py: All data collection scripts
- *_matcher.py: All matching logic scripts
- *_sender.py: All delivery scripts
- *_parser.py: All parsing utilities
- pipeline_orchestrator.py: Main execution script
