# 📁 Project Directory Structure

```
Project/
│
├── 📄 Configuration Files
│   ├── .env                              # Environment variables (API keys, credentials)
│   ├── requirements.txt                  # Python dependencies
│   ├── mcp-server-config.json           # MCP server configuration
│   └── activate_jobly.sh                # Conda environment activation script
│
├── 🤖 Core Pipeline Components
│   ├── run_pipeline.py                  # Main automation pipeline (orchestrates all steps)
│   ├── job_matcher.py                   # AI-powered job matching engine (Gemini 2.0)
│   └── send_email_smtp.py               # Gmail SMTP email delivery
│
├── 🔌 MCP Servers (Claude Desktop Integration)
│   ├── job_matcher_mcp_complete.py      # Full-featured MCP server (RECOMMENDED)
│   ├── job_matcher_mcp_server.py        # Alternative MCP server
│   └── job_matcher_mcp_stdio.py         # STDIO-based MCP server
│
├── 📊 Data Collection Modules
│   │
│   ├── linkedin_collector/              # LinkedIn + The Muse Job Search
│   │   ├── search_and_save.py          # Main entry point for LinkedIn collection
│   │   ├── mcp_server.py               # Async search functions (LinkedIn + The Muse)
│   │   ├── linkedin_searcher.py        # LinkedIn API wrapper
│   │   ├── job_searcher.py             # The Muse Jobs API wrapper
│   │   ├── job_saver.py                # JSON file utilities
│   │   ├── job_keywords.txt            # Search keywords configuration
│   │   ├── job_matcher.py              # Duplicate matcher (can be removed)
│   │   ├── .env                        # LinkedIn credentials
│   │   └── job_search_results/         # Output: LinkedIn job JSONs
│   │       ├── ai_any.json
│   │       ├── artificial_intelligence_any.json
│   │       └── machine_learning_any.json
│   │
│   ├── github_collector/                # GitHub Repository Scraper
│   │   ├── github_fetcher.py           # Main markdown table parser
│   │   ├── github_discovery.py         # Dynamic repo discovery
│   │   └── README.md                   # Documentation
│   │
│   └── API_collector/                   # Web Scraping (Firecrawl)
│       ├── firecrawl_scraper.py        # LLM-powered scraper
│       ├── collect_firecrawl_jobs.py   # Collection script
│       └── test_firecrawl.py           # Testing utilities
│
├── 💾 Data Storage
│   ├── data/                            # Job data from GitHub & other sources
│   │   ├── jobs_output.json            # GitHub jobs (168 jobs)
│   │   └── firecrawl_jobs_*.json       # Firecrawl scraped jobs
│   │
│   └── matched_jobs/                    # AI Matching Results
│       └── top_50_matches.json         # Top 50 ranked job matches
│
├── 📋 Data Models
│   └── models/
│       └── job.py                      # Pydantic Job data model (validation)
│
├── 📄 Resume
│   └── Resume/
│       └── Resume_NEW_ML_Pathakota_Pranavi_2.pdf
│
├── 📚 Documentation
│   ├── README.md                        # Main project documentation
│   ├── DIRECTORY_STRUCTURE.md          # This file
│   ├── MCP_INSPECTOR_GUIDE.md          # MCP testing guide
│   ├── WEB_INSPECTOR_GUIDE.md          # Web scraping guide
│   └── *.md                            # Various setup guides
│
└── 🧪 Testing & Utilities
    ├── test_integration.py              # Integration tests
    └── temp/                           # Temporary files
```

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  1. JOB COLLECTION                          │
├─────────────────────────────────────────────────────────────┤
│ linkedin_collector/    → job_search_results/*.json         │
│ github_collector/      → data/jobs_output.json             │
│ API_collector/         → data/firecrawl_jobs_*.json        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              2. AI MATCHING (job_matcher.py)                │
├─────────────────────────────────────────────────────────────┤
│ • Loads all jobs from sources                               │
│ • Extracts resume text from PDF                             │
│ • Gemini AI scores each job (0-100)                         │
│ • Generates match reasoning                                 │
│ • Saves top 50 → matched_jobs/top_50_matches.json          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           3. EMAIL DELIVERY (send_email_smtp.py)            │
├─────────────────────────────────────────────────────────────┤
│ • Reads matched_jobs/top_50_matches.json                    │
│ • Formats email with job details & scores                   │
│ • Sends via Gmail SMTP                                      │
└─────────────────────────────────────────────────────────────┘
```

## 🔑 Key Files by Function

### Pipeline Orchestration
- **`run_pipeline.py`** - Main automation script that runs all steps sequentially

### Job Collection
- **`linkedin_collector/search_and_save.py`** - LinkedIn + The Muse job search
- **`github_collector/github_fetcher.py`** - GitHub markdown table parser
- **`API_collector/firecrawl_scraper.py`** - Web scraping (optional)

### AI Matching
- **`job_matcher.py`** - Google Gemini AI matching engine
- **`models/job.py`** - Job data validation model

### Communication
- **`send_email_smtp.py`** - Gmail SMTP delivery
- **`job_matcher_mcp_complete.py`** - Claude Desktop MCP integration

### Configuration
- **`.env`** - API keys (Gemini, LinkedIn, Gmail, Firecrawl)
- **`requirements.txt`** - Python package dependencies
- **`mcp-server-config.json`** - MCP server settings

## 📈 Current Job Counts

| Source | Jobs Collected | Output Location |
|--------|---------------|-----------------|
| **LinkedIn** | ~23 per search | `linkedin_collector/job_search_results/` |
| **The Muse** | ~20 per search | Combined with LinkedIn results |
| **GitHub** | 168 jobs | `data/jobs_output.json` |
| **Firecrawl** | 15 jobs | `data/firecrawl_jobs_*.json` |
| **Total** | ~200-300 | Aggregated from all sources |
| **Matched** | Top 50 | `matched_jobs/top_50_matches.json` |

## 🛠️ Technology Stack

- **Python 3.11+** (Conda environment: `jobly`)
- **AI/ML**: Google Gemini 2.0 Flash Experimental
- **APIs**: LinkedIn API, The Muse Jobs API
- **Web Scraping**: Firecrawl, Beautiful Soup, Playwright
- **Data Models**: Pydantic
- **Email**: Gmail SMTP with TLS
- **Protocol**: Model Context Protocol (MCP) for Claude Desktop
- **Async**: asyncio, aiohttp

## 🚀 Entry Points

1. **Full Pipeline**: `python run_pipeline.py`
2. **LinkedIn Collection**: `cd linkedin_collector && python search_and_save.py`
3. **GitHub Collection**: `cd github_collector && python github_fetcher.py`
4. **Job Matching**: `python job_matcher.py`
5. **Send Email**: `python send_email_smtp.py`
6. **MCP Server**: Automatically starts with Claude Desktop

## 📝 Output Files

- **`linkedin_collector/job_search_results/*.json`** - Raw LinkedIn + The Muse jobs
- **`data/jobs_output.json`** - GitHub repository jobs
- **`data/firecrawl_jobs_*.json`** - Web-scraped jobs
- **`matched_jobs/top_50_matches.json`** - AI-matched and ranked jobs

---

**Last Updated**: December 4, 2025  
**Project**: CSCE 689 - Programming LLMs - Automated Job Matcher
