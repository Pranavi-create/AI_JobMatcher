#!/usr/bin/env python3
"""
Complete MCP Server for AI-Powered Job Matching
Works with Claude Desktop

Features:
1. Dynamic job search based on user queries
2. Multi-source collection (LinkedIn, GitHub)
3. AI-powered matching with resume
4. Email delivery of matches
"""

import asyncio
import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from job_matcher import JobMatcher
from dotenv import load_dotenv

# Load environment
load_dotenv()


class JobMatcherMCPComplete:
    """Complete MCP Server for Claude Desktop"""

    def __init__(self):
        self.matcher = JobMatcher()
        self.project_dir = Path(__file__).parent
        self.current_search_query = None
        self.collected_jobs = []
        self.current_matches = []

    async def handle_initialize(self, params: Dict) -> Dict:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "job-matcher",
                "version": "2.0.0"
            }
        }

    async def handle_tools_list(self, params: Dict) -> Dict:
        """List all available tools"""
        return {
            "tools": [
                {
                    "name": "load_jobs",
                    "description": "INSTANT: Load jobs from latest data files without running collectors. Use this for quick access to already collected jobs (recommended for Claude Desktop to avoid timeouts).",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "search_jobs",
                    "description": "FULL SEARCH: Run LinkedIn and GitHub collectors to fetch fresh jobs (takes 5+ minutes, may timeout in Claude Desktop). Use this when you need the latest data and are willing to wait. For instant access, use load_jobs instead.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Search keywords (e.g., ['AI', 'Machine Learning', 'new grad'])"
                            },
                            "location": {
                                "type": "string",
                                "description": "Job location (e.g., 'USA', 'Remote', 'San Francisco')"
                            },
                            "job_type": {
                                "type": "string",
                                "description": "Type of position (e.g., 'new_grad', 'internship', 'full-time')"
                            }
                        },
                        "required": ["keywords"]
                    }
                },
                {
                    "name": "get_job_statistics",
                    "description": "Get statistics about currently collected jobs (total count, sources, breakdown)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                },
                {
                    "name": "match_jobs_with_resume",
                    "description": "Use AI to match collected jobs with user's resume. Returns ranked matches with scores and reasoning.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "resume_path": {
                                "type": "string",
                                "description": "Path to resume PDF file (optional, uses default if not provided)"
                            },
                            "top_n": {
                                "type": "number",
                                "description": "Number of top matches to return (default: 10)",
                                "default": 10
                            },
                            "min_score": {
                                "type": "number",
                                "description": "Minimum match score threshold 0-100 (default: 60)",
                                "default": 60
                            }
                        }
                    }
                },
                {
                    "name": "get_match_details",
                    "description": "Get detailed analysis of why a specific job matches or doesn't match the resume",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "job_index": {
                                "type": "number",
                                "description": "Index of the job to analyze (from matched results)"
                            }
                        },
                        "required": ["job_index"]
                    }
                },
                {
                    "name": "send_matches_email",
                    "description": "Send top job matches via email using Gmail SMTP. Ask user for their email address.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "recipient": {
                                "type": "string",
                                "description": "Email address to send matches to (REQUIRED - must ask user)"
                            },
                            "top_n": {
                                "type": "number",
                                "description": "Number of matches to send (default: 50)",
                                "default": 50
                            }
                        },
                        "required": ["recipient"]
                    }
                },
                {
                    "name": "update_linkedin_jobs",
                    "description": "Trigger LinkedIn job collection with specific search terms",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Keywords to search on LinkedIn"
                            }
                        },
                        "required": ["keywords"]
                    }
                },
                {
                    "name": "update_github_jobs",
                    "description": "Trigger GitHub repository job collection",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "search_terms": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Search terms for GitHub repos (e.g., ['2026 new grad jobs', '2026 AI jobs'])"
                            }
                        },
                        "required": ["search_terms"]
                    }
                }
            ]
        }

    async def handle_tools_call(self, params: Dict) -> Dict:
        """Execute a tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "load_jobs":
                result = await self._load_jobs(arguments)
            elif tool_name == "search_jobs":
                result = await self._search_jobs(arguments)
            elif tool_name == "get_job_statistics":
                result = await self._get_statistics(arguments)
            elif tool_name == "match_jobs_with_resume":
                result = await self._match_jobs(arguments)
            elif tool_name == "get_match_details":
                result = await self._get_match_details(arguments)
            elif tool_name == "send_matches_email":
                result = await self._send_email(arguments)
            elif tool_name == "update_linkedin_jobs":
                result = await self._update_linkedin(arguments)
            elif tool_name == "update_github_jobs":
                result = await self._update_github(arguments)
            else:
                result = f"❌ Unknown tool: {tool_name}"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": result if isinstance(result, str) else json.dumps(result, indent=2)
                    }
                ]
            }

        except Exception as e:
            import traceback
            error_msg = f"❌ Error executing {tool_name}: {str(e)}\n\n{traceback.format_exc()}"
            return {
                "content": [
                    {
                        "type": "text",
                        "text": error_msg
                    }
                ],
                "isError": True
            }

    async def _load_jobs(self, args: Dict) -> str:
        """Load jobs from latest collected data files (INSTANT - no collection)"""
        try:
            result_msg = "📂 LOADING JOBS FROM LATEST DATA FILES\n"
            result_msg += "="*60 + "\n\n"
            
            jobs_dirs = [
                str(self.project_dir / "linkedin_collector" / "data"),
                str(self.project_dir / "github_collector" / "data"),
                str(self.project_dir / "API_collector" / "data")
            ]
            
            # Load from most recent files
            self.collected_jobs = self.matcher.load_all_jobs(jobs_dirs)
            
            result_msg += f"✅ Loaded {len(self.collected_jobs)} jobs\n\n"
            
            # Show breakdown by source
            sources = {}
            for job in self.collected_jobs:
                source = job.get("source", "Unknown")
                sources[source] = sources.get(source, 0) + 1
            
            result_msg += "📊 Jobs by Source:\n"
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                result_msg += f"   • {source}: {count} jobs\n"
            
            # Show which files were loaded
            result_msg += "\n📁 Latest Files Loaded:\n"
            for jobs_dir in jobs_dirs:
                dir_path = Path(jobs_dir)
                if dir_path.exists():
                    json_files = sorted(dir_path.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
                    if json_files:
                        latest = json_files[0]
                        result_msg += f"   • {dir_path.name}: {latest.name}\n"
                    else:
                        result_msg += f"   • {dir_path.name}: (no files)\n"
            
            result_msg += "\n" + "="*60 + "\n"
            result_msg += f"✅ Jobs Ready!\n\n"
            result_msg += f"💡 Next: Use 'match_jobs_with_resume' to find best matches!\n"
            result_msg += f"💡 Or: Use 'get_job_statistics' for detailed breakdown\n"
            
            return result_msg
            
        except Exception as e:
            import traceback
            return f"❌ Error loading jobs: {str(e)}\n\n{traceback.format_exc()}"

    async def _search_jobs(self, args: Dict) -> str:
        """ACTUALLY search for new jobs by running collectors (may take 5+ minutes)"""
        keywords = args.get("keywords", [])
        location = args.get("location", "")
        job_type = args.get("job_type", "")

        self.current_search_query = {
            "keywords": keywords,
            "location": location,
            "job_type": job_type
        }

        result_msg = "🔍 JOB SEARCH IN PROGRESS\n"
        result_msg += "="*60 + "\n\n"
        result_msg += f"🎯 Search Parameters:\n"
        result_msg += f"   • Keywords: {', '.join(keywords)}\n"
        if location:
            result_msg += f"   • Location: {location}\n"
        if job_type:
            result_msg += f"   • Type: {job_type}\n"
        result_msg += "\n"

        # Run LinkedIn collector
        result_msg += await self._run_linkedin_collector({"keywords": keywords})
        result_msg += "\n"

        # Run GitHub collector
        result_msg += await self._run_github_collector({"keywords": keywords})
        result_msg += "\n"

        # Now load all collected jobs
        result_msg += "📂 Loading collected jobs...\n"
        jobs_dirs = [
            str(self.project_dir / "linkedin_collector" / "data"),
            str(self.project_dir / "github_collector" / "data"),
            str(self.project_dir / "API_collector" / "data")
        ]
        
        self.collected_jobs = self.matcher.load_all_jobs(jobs_dirs)
        
        result_msg += f"✅ Loaded {len(self.collected_jobs)} total jobs\n\n"
        
        # Show breakdown by source
        sources = {}
        for job in self.collected_jobs:
            source = job.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1
        
        result_msg += "📊 Jobs by Source:\n"
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            result_msg += f"   • {source}: {count} jobs\n"
        
        result_msg += "\n" + "="*60 + "\n"
        result_msg += f"✅ Search Complete! Found {len(self.collected_jobs)} jobs\n\n"
        result_msg += f"💡 Next: Use 'match_jobs_with_resume' to find best matches!\n"
        
        return result_msg

    async def _run_linkedin_collector(self, args: Dict) -> str:
        """ACTUALLY RUN the LinkedIn collector"""
        keywords = args.get("keywords", [])

        try:
            # Update keywords file
            keywords_file = self.project_dir / "linkedin_collector" / "job_keywords.txt"
            with open(keywords_file, 'w') as f:
                f.write('\n'.join(keywords))

            result = f"✅ LinkedIn keywords set: {', '.join(keywords)}\n"
            result += f"🔄 Running LinkedIn collector...\n"

            # ACTUALLY RUN the LinkedIn collector using jobly environment
            linkedin_script = self.project_dir / "linkedin_collector" / "linkedin_scraper.py"
            proc_result = subprocess.run([
                "/opt/anaconda3/envs/jobly/bin/python",
                str(linkedin_script)
            ], capture_output=True, text=True, timeout=300)  # Increased to 5 minutes

            if proc_result.returncode == 0:
                result += f"✅ LinkedIn collection completed!\n"
                # Get the most recent file
                results_dir = self.project_dir / "linkedin_collector" / "data"
                json_files = sorted(results_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
                if json_files:
                    latest_file = json_files[0]
                    result += f"📊 Latest file: {latest_file.name}\n"
                    result += f"   (Total files in data/: {len(json_files)})\n"
            else:
                result += f"⚠️ LinkedIn collector finished with warnings\n"
                result += f"   Using existing data\n"

            return result

        except subprocess.TimeoutExpired:
            return "⏱️ LinkedIn collector timed out - using existing data\n"
        except Exception as e:
            return f"⚠️ LinkedIn collector error: {str(e)}\n   Using existing data\n"

    async def _run_github_collector(self, args: Dict) -> str:
        """ACTUALLY RUN the GitHub collector"""
        keywords = args.get("keywords", [])

        try:
            result = f"🔄 Running GitHub job collector...\n"

            # ACTUALLY RUN the GitHub collector using jobly environment
            github_script = self.project_dir / "github_collector" / "github_fetcher.py"
            proc_result = subprocess.run([
                "/opt/anaconda3/envs/jobly/bin/python",
                str(github_script)
            ], capture_output=True, text=True, timeout=180)  # Increased to 3 minutes

            if proc_result.returncode == 0:
                result += f"✅ GitHub collection completed!\n"
                # Count jobs from data
                data_file = self.project_dir / "data" / "jobs_output.json"
                if data_file.exists():
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                        # Handle both list and dict formats
                        if isinstance(data, list):
                            count = len(data)
                        elif isinstance(data, dict):
                            count = len(data.get('jobs', []))
                        else:
                            count = 0
                        result += f"📊 Found {count} jobs from GitHub repos\n"
            else:
                result += f"⚠️ GitHub collector finished with warnings\n"
                result += f"   Using existing data\n"

            return result

        except subprocess.TimeoutExpired:
            return "⏱️ GitHub collector timed out - using existing data\n"
        except Exception as e:
            return f"⚠️ GitHub collector error: {str(e)}\n   Using existing data\n"

    async def _update_linkedin(self, args: Dict) -> str:
        """Update LinkedIn jobs (old method - redirects to run)"""
        return await self._run_linkedin_collector(args)

    async def _update_github(self, args: Dict) -> str:
        """Update GitHub jobs (old method - redirects to run)"""
        return await self._run_github_collector(args)

    async def _get_statistics(self, args: Dict) -> str:
        """Get job statistics"""
        try:
            jobs_dirs = [
                str(self.project_dir / "linkedin_collector" / "data"),
                str(self.project_dir / "github_collector" / "data"),
                str(self.project_dir / "API_collector" / "data")
            ]
            jobs = self.matcher.load_all_jobs(jobs_dirs)

            sources = {}
            locations = {}
            for job in jobs:
                source = job.get("source", "Unknown")
                sources[source] = sources.get(source, 0) + 1

                location = job.get("location", "Unknown")
                locations[location] = locations.get(location, 0) + 1

            result = "📊 JOB STATISTICS\n"
            result += "="*60 + "\n\n"
            result += f"📈 Total Jobs: {len(jobs)}\n\n"

            result += "📍 By Source:\n"
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"   • {source}: {count} jobs\n"

            result += f"\n🌍 Top Locations:\n"
            for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"   • {location}: {count} jobs\n"

            if self.current_search_query:
                result += f"\n🔍 Current Search Query:\n"
                result += f"   • Keywords: {', '.join(self.current_search_query['keywords'])}\n"
                if self.current_search_query.get('location'):
                    result += f"   • Location: {self.current_search_query['location']}\n"
                if self.current_search_query.get('job_type'):
                    result += f"   • Type: {self.current_search_query['job_type']}\n"

            result += f"\n📋 Sample Jobs:\n"
            for i, job in enumerate(jobs[:3], 1):
                result += f"\n{i}. {job.get('position', 'N/A')} at {job.get('company', 'N/A')}\n"
                result += f"   Location: {job.get('location', 'N/A')}\n"
                result += f"   Source: {job.get('source', 'N/A')}\n"

            return result

        except Exception as e:
            return f"❌ Error getting statistics: {str(e)}"

    async def _match_jobs(self, args: Dict) -> str:
        """Match jobs with resume using AI"""
        try:
            resume_path = args.get("resume_path")
            if not resume_path:
                # Use default resume from resume folder
                resume_path = str(self.project_dir / "resume" / "Resume_NEW_ML_Pathakota_Pranavi_2.pdf")

            top_n = args.get("top_n", 10)
            min_score = args.get("min_score", 60)

            result = "🤖 AI JOB MATCHING\n"
            result += "="*60 + "\n\n"
            result += f"📄 Resume: {Path(resume_path).name}\n"
            result += f"🎯 Finding top {top_n} matches (min score: {min_score})\n\n"

            # Use jobs from current search session if available, otherwise load from disk
            if self.collected_jobs:
                all_jobs = self.collected_jobs
                result += f"📊 Using {len(all_jobs)} jobs from current search session\n\n"
            else:
                # Fallback: Load jobs from disk
                jobs_dirs = [
                    str(self.project_dir / "linkedin_collector" / "data"),
                    str(self.project_dir / "github_collector" / "data"),
                    str(self.project_dir / "API_collector" / "data")
                ]
                all_jobs = self.matcher.load_all_jobs(jobs_dirs)
                result += f"📊 Analyzing {len(all_jobs)} jobs from disk (no current search)\n\n"

            # Extract resume - FIXED: use correct method name
            resume_text = self.matcher.extract_text_from_pdf(resume_path)
            result += f"✅ Resume extracted ({len(resume_text)} chars)\n\n"

            result += "⏳ Matching with AI (this may take a moment)...\n\n"

            # Use the built-in LLM matching from JobMatcher
            top_matches = self.matcher.match_jobs_with_llm(resume_text, all_jobs[:100], top_n=top_n)

            # Filter by min score
            top_matches = [job for job in top_matches if job.get('match_score', 0) >= min_score]

            result += "\n" + "="*60 + "\n"
            result += f"🎯 TOP {len(top_matches)} JOB MATCHES\n"
            result += "="*60 + "\n\n"

            for i, match in enumerate(top_matches, 1):
                result += f"{i}. {match.get('position', 'Unknown')} at {match.get('company', 'Unknown')}\n"
                result += f"   📍 Location: {match.get('location', 'N/A')}\n"
                result += f"   ⭐ Score: {match.get('match_score', 0)}/100\n"
                result += f"   💡 Why: {match.get('match_reason', 'N/A')}\n"
                result += f"   🔗 Apply: {match.get('apply_link', 'N/A')}\n\n"

            # Save matches for email
            self.current_matches = top_matches

            result += "="*60 + "\n"
            result += f"📧 To send these via email, use 'send_matches_email'\n"

            return result

        except Exception as e:
            import traceback
            return f"❌ Error matching jobs: {str(e)}\n\n{traceback.format_exc()}"

    async def _get_match_details(self, args: Dict) -> str:
        """Get detailed match analysis"""
        job_index = args.get("job_index", 0)

        try:
            jobs_dirs = [
                str(self.project_dir / "linkedin_collector" / "data"),
                str(self.project_dir / "github_collector" / "data"),
                str(self.project_dir / "API_collector" / "data")
            ]
            all_jobs = self.matcher.load_all_jobs(jobs_dirs)

            if job_index >= len(all_jobs):
                return f"❌ Job index {job_index} out of range (max: {len(all_jobs)-1})"

            job = all_jobs[job_index]

            result = "🔍 DETAILED JOB ANALYSIS\n"
            result += "="*60 + "\n\n"
            result += f"Position: {job.get('position', 'N/A')}\n"
            result += f"Company: {job.get('company', 'N/A')}\n"
            result += f"Location: {job.get('location', 'N/A')}\n"
            result += f"Source: {job.get('source', 'N/A')}\n"
            result += f"Link: {job.get('apply_link', 'N/A')}\n\n"

            if job.get('description'):
                result += f"Description:\n{job['description'][:500]}...\n\n"

            return result

        except Exception as e:
            return f"❌ Error getting match details: {str(e)}"

    async def _send_email(self, args: Dict) -> str:
        """Send matches via email"""
        try:
            recipient = args.get("recipient")
            if not recipient:
                return "❌ Recipient email address is required. Please provide the email address where you'd like to receive the job matches."

            top_n = args.get("top_n", 50)

            result = f"📧 Preparing to send top {top_n} matches to {recipient}...\n\n"

            # Check if we have current matches from this session
            if self.current_matches:
                result += f"✅ Using {len(self.current_matches)} matches from current search session\n\n"
                matches_to_send = self.current_matches[:top_n]
                
                # Save these matches to the standard location for email script
                matched_jobs_file = self.project_dir / "matched_jobs" / "top_50_matches.json"
                matched_jobs_file.parent.mkdir(exist_ok=True)
                
                match_data = {
                    "matched_jobs": matches_to_send,
                    "total_matched": len(matches_to_send),
                    "search_query": self.current_search_query,
                    "matched_at": datetime.now().isoformat()
                }
                
                with open(matched_jobs_file, 'w') as f:
                    json.dump(match_data, f, indent=2)
                
                result += f"💾 Saved {len(matches_to_send)} matches for email\n\n"
            else:
                # Fallback: check if we have matches saved from previous runs
                matched_jobs_file = self.project_dir / "matched_jobs" / "top_50_matches.json"
                if not matched_jobs_file.exists():
                    result += "⚠️ No matched jobs found. Please run 'match_jobs_with_resume' first.\n"
                    return result
                result += "⚠️ Using matches from previous session (no current matches available)\n\n"

            # Update recipient in send_email_smtp.py temporarily via env
            import os
            os.environ['RECIPIENT_EMAIL'] = recipient

            # Run the email script using jobly environment
            email_script = self.project_dir / "send_email_smtp.py"
            email_result = subprocess.run([
                "/opt/anaconda3/envs/jobly/bin/python",
                str(email_script)
            ], capture_output=True, text=True)

            if email_result.returncode == 0:
                result += "✅ Email sent successfully!\n"
                result += f"📬 Check your inbox: {recipient}\n"
                result += "\n📧 Email contains:\n"
                result += f"   • Top {len(matches_to_send) if self.current_matches else top_n} job matches\n"
                result += f"   • Match scores and reasoning\n"
                result += f"   • Direct application links\n"
            else:
                result += f"❌ Email sending failed:\n{email_result.stderr}\n"

            return result

        except Exception as e:
            import traceback
            return f"❌ Error sending email: {str(e)}\n\n{traceback.format_exc()}"

    async def process_request(self, request: Dict) -> Dict:
        """Process a single MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "tools/list":
                result = await self.handle_tools_list(params)
            elif method == "tools/call":
                result = await self.handle_tools_call(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        except Exception as e:
            import traceback
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}\n{traceback.format_exc()}"
                }
            }

    async def run(self):
        """Main server loop - stdio communication"""
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)

        print("🚀 Job Matcher MCP Server v2.0 started", file=sys.stderr)
        print("Ready for Claude Desktop", file=sys.stderr)

        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                line = line.strip()
                if not line:
                    continue

                request = json.loads(line)
                response = await self.process_request(request)
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr)
                continue
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                continue


async def main():
    """Entry point"""
    server = JobMatcherMCPComplete()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
