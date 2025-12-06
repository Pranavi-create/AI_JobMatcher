# 🎯 Automated Job Matcher & Email System

An intelligent end-to-end job application pipeline that collects jobs from multiple sources, matches them with your resume using AI, and emails the top matches.

## ✨ Features

- **Multi-Source Job Collection**: Automatically collects jobs from LinkedIn and GitHub repositories
- **AI-Powered Matching**: Uses Google Gemini AI to match jobs with your resume
- **Smart Ranking**: Ranks jobs by relevance with detailed match reasoning
- **Automated Email Delivery**: Sends top 50 job matches via Gmail SMTP
- **Complete Automation**: One command runs the entire pipeline

## 📁 Project Structure

```
Project/
├── linkedin_collector/          # LinkedIn job collection
│   ├── linkedin_searcher.py     # LinkedIn API search
│   ├── linkedin_scraper.py      # Main search orchestrator
│   ├── linkedin_job_aggregator.py  # Combines LinkedIn + Muse APIs
│   ├── muse_api_client.py       # The Muse API integration
│   ├── job_keywords.txt         # Search keywords (pipe-delimited)
│   └── data/                    # LinkedIn job data (timestamped)
│
├── github_collector/            # GitHub job collection
│   ├── github_discovery.py      # Discover job repos
│   ├── github_fetcher.py        # Fetch GitHub jobs
│   └── data/                    # GitHub job data (timestamped)
│
├── API_collector/               # Firecrawl web scraping
│   ├── firecrawl_scraper.py     # LLM-powered scraper
│   ├── collect_firecrawl_jobs.py  # Main collector
│   └── data/                    # Firecrawl job data (timestamped)
│
├── matched_jobs/                # AI matching results
│   └── top_50_matches.json      # Top 50 ranked jobs
│
├── models/                      # Data models
│   └── job.py                   # Job data structure
│
├── resume/                      # Resume folder
│   └── Resume_NEW_ML_Pathakota_Pranavi_2.pdf  # Your resume
│
├── job_matcher.py              # AI job matching engine
├── job_matcher_mcp_complete.py # MCP server (LIVE searches)
├── job_matcher_mcp_server.py   # MCP server (pre-computed data)
├── job_matcher_mcp_stdio.py    # MCP server (testing/debugging)
├── send_email_smtp.py          # Gmail email sender
├── run_pipeline.py             # Main automation pipeline
├── mcp-server-config.json      # Claude Desktop MCP config
└── .env                        # Configuration (API keys)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright for web scraping (if needed)
playwright install chromium
```

### 2. Configure Environment Variables

Edit `.env` file with your credentials:

```bash
# Gemini API Key (REQUIRED for job matching)
GEMINI_API_KEY=your_gemini_api_key_here

# LinkedIn Credentials (for LinkedIn job search)
LINKEDIN_EMAIL=your_linkedin_email@gmail.com
LINKEDIN_PASSWORD=your_linkedin_password

# Gmail SMTP (REQUIRED for email sending)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=recipient@gmail.com

# Firecrawl API (OPTIONAL - for web scraping)
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

#### Get Gmail App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Create password for "Mail"
3. Copy the 16-character password (remove spaces)
4. Add to `.env` file

#### Get Gemini API Key:
1. Go to https://aistudio.google.com/app/apikey
2. Create API key
3. Add to `.env` file

### 3. Run the Complete Pipeline

```bash
python3 run_pipeline.py
```

This will:
1. ✅ Collect jobs from LinkedIn, GitHub, and other sources
2. 🤖 Match jobs with your resume using AI
3. 📊 Rank and select top 50 matches
4. 📧 Send email with job details

## 📋 Pipeline Components

### 1. Job Collection

**LinkedIn Collector** (`linkedin_collector/`)
- Searches LinkedIn for relevant jobs using LinkedIn API
- Also searches The Muse Jobs API (combined search)
- Saves to `linkedin_collector/data/` with timestamps
- Configure search keywords in `linkedin_collector/job_keywords.txt`
  - Format: `keyword | location | limit`
  - Example: `machine learning engineer | Remote | 30`

```bash
cd linkedin_collector
python3 linkedin_scraper.py
```

**GitHub Collector** (`github_collector/`)
- Discovers job repositories on GitHub
- Fetches jobs from curated markdown tables (SimplifyJobs, etc.)
- Saves to `github_collector/data/` with timestamps

```bash
cd github_collector
python3 github_fetcher.py
```

**Firecrawl Collector** (`API_collector/`) - Optional
- LLM-powered web scraping for JobRight.ai, Simplify.jobs, Wellfound
- Requires `FIRECRAWL_API_KEY` in `.env`
- Saves to `API_collector/data/` with timestamps

```bash
cd API_collector
python3 collect_firecrawl_jobs.py
```

### Important: Data Loading Strategy

**To avoid duplicates**, the system now loads **only the most recent file** from each collector's data folder:
- `linkedin_collector/data/` → Latest file only
- `github_collector/data/` → Latest file only
- `API_collector/data/` → Latest file only

Old files are kept as backup/history but not loaded during job matching.

### 2. AI Job Matching

**Job Matcher** (`job_matcher.py`)
- Loads jobs from all sources
- Extracts resume from PDF
- Uses Gemini AI to:
  - Calculate match scores (0-100)
  - Provide match reasoning
  - Rank jobs by relevance

```bash
python3 job_matcher.py
```

Output: `matched_jobs/top_50_matches.json`

### 3. Email Delivery

**SMTP Email Sender** (`send_email_smtp.py`)
- Sends top matches via Gmail
- Formats jobs in readable email
- Includes apply links and match scores

```bash
python3 send_email_smtp.py
```

## 🔧 Individual Component Usage

### View Collected Jobs

```bash
python3 view_jobs.py
```

Shows statistics:
- Total jobs collected
- Jobs by source
- Sample job listings

### Run Job Matcher Only

```bash
python3 job_matcher.py
```

Outputs:
- Console: Match scores and reasoning
- File: `matched_jobs/top_50_matches.json`

### Test Email Sending

```bash
python3 send_email_smtp.py
```

Requires:
- `matched_jobs/top_50_matches.json` to exist
- Gmail credentials in `.env`

## 📊 Output Format

### Matched Jobs (`matched_jobs/top_50_matches.json`)

```json
{
  "matched_jobs": [
    {
      "company": "Google",
      "position": "Machine Learning Engineer",
      "location": "Mountain View, CA",
      "match_score": 95,
      "match_reason": "Strong alignment with your ML background...",
      "apply_link": "https://...",
      "source": "LinkedIn"
    }
  ],
  "total_matched": 50,
  "resume_summary": "...",
  "matched_at": "2025-11-09T10:30:00"
}
```

### Email Format

```
🎯 Top Job Matches Based on Your Resume
======================================================================

1. Machine Learning Engineer
   Company: Google
   Location: Mountain View, CA
   Match Score: 95/100
   Why: Strong alignment with your ML background and experience...
   Apply: https://...

[... 49 more jobs ...]
```

## 🔑 Configuration

### Resume Location

Update in `job_matcher.py` (line 291):
```python
resume_pdf = str(project_dir / "resume" / "YOUR_RESUME_FILE.pdf")
```


### Job Sources

Add/modify sources in collectors:
- LinkedIn: `linkedin_collector/linkedin_scraper.py`
- GitHub: `github_collector/github_discovery.py`
- Firecrawl: `API_collector/collect_firecrawl_jobs.py`

### Job Keywords Configuration

Edit `linkedin_collector/job_keywords.txt` with pipe-delimited format:
```
machine learning engineer | Remote | 30
AI engineer | San Francisco | 20
data scientist | New York | 25
```

Format: `keyword | location | limit`
- Leave location empty for all locations
- Default limit is 30 if not specified

### Email Settings

Configure in `.env`:
```bash
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=recipient_email@gmail.com
```

### AI Model

Change model in `job_matcher.py` (line 35):
```python
self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
```

## 🛠️ Troubleshooting

### "No matched jobs found"
- Check if `matched_jobs/top_50_matches.json` exists
- Run `python3 job_matcher.py` first

### Email not sending
- Verify Gmail App Password is correct (16 chars, no spaces)
- Check 2-Factor Authentication is enabled
- Check spam folder for received emails

### "GEMINI_API_KEY not found"
- Add your Gemini API key to `.env` file
- Get key at: https://aistudio.google.com/app/apikey

### Job collection fails
- Check internet connection
- Verify API tokens in `.env`
- Check rate limits for LinkedIn/GitHub

### Claude Desktop shows "Using existing data"
- **Fixed in latest version!** Update your code.
- Restart Claude Desktop after code changes
- Check that `linkedin_scraper.py` exists

### Getting duplicate jobs
- **Fixed in latest version!** Update your code.
- System now loads only the most recent file from each data folder
- Old files are kept as history but not loaded

### Too many old JSON files in data folders
**Optional cleanup:**
```bash
# View files by date (newest first)
cd linkedin_collector/data && ls -lht

# Keep latest, delete old ones (optional)
# Be careful - this deletes files permanently!
cd linkedin_collector/data
ls -t *.json | tail -n +2 | xargs rm  # Keeps newest, deletes rest
```

**Or keep all for history** - they won't cause duplicates anymore!

## 📈 Pipeline Flow

```
┌─────────────────────────────────────────────────┐
│  1. JOB COLLECTION                              │
│  ─────────────────                              │
│  • LinkedIn Collector → job_search_results/     │
│  • GitHub Collector   → data/jobs_output.json   │
│  • Other Sources      → data/                   │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  2. AI JOB MATCHING (job_matcher.py)            │
│  ────────────────────────────────                │
│  • Load all collected jobs from sources         │
│  • Extract resume from PDF                      │
│  • Gemini AI analyzes each job                  │
│  • Calculate match scores (0-100)               │
│  • Generate match reasoning                     │
│  • Rank and select top 50                       │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  3. EMAIL DELIVERY (send_email_smtp.py)         │
│  ───────────────────────────────────             │
│  • Load top 50 matches                          │
│  • Format email with job details                │
│  • Send via Gmail SMTP                          │
│  • ✅ Check your inbox!                         │
└─────────────────────────────────────────────────┘
```


## 📝 Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `run_pipeline.py` | Complete automation | Run entire pipeline |
| `job_matcher.py` | AI matching engine | Match jobs with resume |
| `send_email_smtp.py` | Email sender | Send matched jobs |


## 🤖 Claude Desktop Integration (MCP Servers)

This project includes **Model Context Protocol (MCP)** servers for Claude Desktop integration. Choose the one that fits your needs:

### 1️⃣ `job_matcher_mcp_complete.py` - RECOMMENDED for Claude Desktop
**Live Job Searches**
- ✅ Runs collectors LIVE via subprocess
- ✅ Gets fresh data every search
- ✅ Full-featured with all tools
- ⏱️ Takes 5+ minutes per search
- 🎯 Best for: Interactive Claude Desktop sessions

**Tools Available:**
- `search_jobs` - Run LinkedIn + GitHub collectors with keywords
- `match_jobs_with_resume` - AI matching with Gemini
- `send_top_matches_email` - Email delivery
- `get_statistics` - View job stats
- `analyze_job_match` - Deep dive on specific jobs

### 2️⃣ `job_matcher_mcp_server.py` - Pre-computed Data
**Fast Queries on Existing Data**
- 📁 Loads from existing JSON files
- ⚡ Instant results
- 🎯 Best for: Quick analysis of collected data

### 3️⃣ `job_matcher_mcp_stdio.py` - Testing/Debugging
**Minimal STDIO Protocol**
- 📁 Loads from existing JSON files
- 🔧 Best for: MCP Inspector testing

### Claude Desktop Configuration

Your `mcp-server-config.json` is configured to use the complete version:

```json
{
  "mcpServers": {
    "job-matcher": {
      "command": "/opt/anaconda3/envs/jobly/bin/python",
      "args": [
        "/job_matcher_mcp_complete.py"
      ],
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

**To use Claude Desktop:**
1. Restart Claude Desktop after any code changes
2. Use natural language: "Search for AI jobs and match with my resume"
3. Claude will call the appropriate MCP tools automatically

## � Recent Updates

### ✅ Fixed: Duplicate Jobs Issue (Dec 6, 2025)
**Problem:** System was loading ALL JSON files from data folders, causing duplicates.

**Solution:** Modified `job_matcher.py` to load **only the most recent file** from each collector:
```python
# Now loads only the newest timestamped file
json_files = sorted(jobs_path.glob("*.json"), 
                   key=lambda x: x.stat().st_mtime, 
                   reverse=True)
if json_files:
    json_files = [json_files[0]]  # Only most recent
```


**Result:** Claude Desktop now performs LIVE searches successfully.


## �🚦 Status

✅ **Job Collection**: Working (LinkedIn + GitHub + The Muse + Firecrawl)
✅ **AI Matching**: Working (Gemini 2.5 Flash)
✅ **Email Sending**: Working (Gmail SMTP)
✅ **Claude Desktop MCP**: Working (Live searches)
✅ **Full Pipeline**: Ready to use


