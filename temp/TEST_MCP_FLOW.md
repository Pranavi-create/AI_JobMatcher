# MCP Server Flow Verification

## ✅ What the MCP Server Does (When Used from Claude Desktop)

### Tool: `search_jobs`
**What it ACTUALLY does:**
1. ✅ **Runs LinkedIn Collector** - Executes `linkedin_collector/search_and_save.py` with your keywords
   - Uses real LinkedIn API to fetch live jobs
   - Saves to `linkedin_collector/job_search_results/`
   
2. ✅ **Runs GitHub Collector** - Executes `github_collector/github_fetcher.py`
   - Fetches jobs from GitHub repositories (speedyapply/2026-AI-College-Jobs)
   - Saves to `data/jobs_output.json`
   
3. ✅ **Loads Fresh Data** - Reads the newly collected job files
   - NOT loading old cached data
   - Loads from directories that were JUST updated

**Example Claude Command:**
```
Search for AI and Machine Learning jobs in Remote locations
```

---

### Tool: `match_jobs_with_resume`
**What it ACTUALLY does:**
1. ✅ **Extracts Resume** - Reads your PDF resume from `Resume/` folder
2. ✅ **Uses AI Matching** - Sends resume + job descriptions to Google Gemini LLM
3. ✅ **Ranks Jobs** - Returns top N matches with scores and reasoning
4. ✅ **Saves Results** - Writes to `matched_jobs/top_50_matches.json`

**Example Claude Command:**
```
Match the collected jobs with my resume and show me the top 10
```

---

### Tool: `send_job_matches_email`
**What it ACTUALLY does:**
1. ✅ **Checks for Matches** - Verifies `matched_jobs/top_50_matches.json` exists
   - If missing, automatically runs `job_matcher.py` first
2. ✅ **Sends Email** - Uses Gmail SMTP to send formatted email
3. ✅ **Includes Details** - Job titles, companies, match scores, links

**Example Claude Command:**
```
Email me the top 50 matched jobs at pranavipathakota@gmail.com
```

---

## 🔄 Complete Workflow Example

**In Claude Desktop, you would say:**

```
1. "Search for Data Scientist and ML Engineer jobs"
   → Runs LinkedIn + GitHub collectors
   → Collects fresh jobs

2. "Match these jobs with my resume"
   → Uses AI to rank jobs
   → Saves top 50 matches

3. "Email me the results"
   → Sends formatted email with matches
```

---

## ⚙️ Technical Details

### Environment
- Python: `/opt/anaconda3/envs/jobly/bin/python`
- All dependencies installed in `jobly` conda environment
- Uses real LinkedIn API (not simulated data)

### File Locations
- LinkedIn Results: `linkedin_collector/job_search_results/*.json`
- GitHub Results: `data/jobs_output.json`
- Matched Jobs: `matched_jobs/top_50_matches.json`
- Resume: `Resume/*.pdf`

### Key Points
✅ **DOES** run collectors every time `search_jobs` is called
✅ **DOES** use real LinkedIn API with your credentials
✅ **DOES** fetch fresh GitHub jobs
✅ **DOES** use AI to match with resume
❌ **DOES NOT** just load old cached data
❌ **DOES NOT** use simulated/fake jobs

---

## 🧪 How to Test

1. **Delete old job files** to verify fresh collection:
```bash
rm -rf linkedin_collector/job_search_results/*.json
rm -f data/jobs_output.json
```

2. **In Claude Desktop**, run:
```
Search for Software Engineer jobs in San Francisco
```

3. **Verify** new files were created with today's timestamp

4. **Check file contents** to see they contain real LinkedIn job IDs and GitHub jobs
