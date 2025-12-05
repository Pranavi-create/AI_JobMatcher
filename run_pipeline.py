#!/usr/bin/env python3
"""
Complete Job Application Pipeline
1. Collect jobs from LinkedIn (real API)
2. Collect jobs from GitHub repositories
3. Match jobs with resume using LLM
4. Send top 50 matches via Gmail
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()


def collect_linkedin_jobs():
    """Step 1: Collect jobs from LinkedIn"""
    print("\n" + "=" * 70)
    print("📊 STEP 1: COLLECTING JOBS FROM LINKEDIN")
    print("=" * 70)

    try:
        linkedin_dir = Path(__file__).parent / "linkedin_collector"
        result = subprocess.run(
            ["python", "search_and_save.py"],
            cwd=linkedin_dir,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("⚠️  LinkedIn collection had issues (continuing anyway)")
            return False

        print("\n✅ LinkedIn job collection completed!")
        return True

    except Exception as e:
        print(f"❌ Error collecting LinkedIn jobs: {e}")
        return False


def collect_github_jobs():
    """Step 2: Collect jobs from GitHub repositories"""
    print("\n" + "=" * 70)
    print("📚 STEP 2: COLLECTING JOBS FROM GITHUB")
    print("=" * 70)

    try:
        github_dir = Path(__file__).parent / "github_collector"
        result = subprocess.run(
            ["python", "github_fetcher.py"],
            cwd=github_dir,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("⚠️  GitHub collection had issues (continuing anyway)")
            return False

        print("\n✅ GitHub job collection completed!")
        return True

    except Exception as e:
        print(f"❌ Error collecting GitHub jobs: {e}")
        return False


def collect_firecrawl_jobs():
    """Step 3: Collect jobs from web sources via Firecrawl (optional)"""
    print("\n" + "=" * 70)
    print("🔥 STEP 3: COLLECTING JOBS VIA FIRECRAWL (WEB SCRAPING)")
    print("=" * 70)

    try:
        # Check if Firecrawl API key exists
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            print("⚠️  FIRECRAWL_API_KEY not set - skipping web scraping")
            print("   (This is optional - other collectors will still work)")
            return True  # Not an error, just skipped

        api_collector_dir = Path(__file__).parent / "API_collector"
        result = subprocess.run(
            ["python", "collect_firecrawl_jobs.py"],
            cwd=api_collector_dir,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("⚠️  Firecrawl collection had issues (continuing anyway)")
            print("   LinkedIn and GitHub collections are still available")
            return True  # Don't fail pipeline

        print("\n✅ Firecrawl job collection completed!")
        return True

    except Exception as e:
        print(f"⚠️  Firecrawl collection skipped: {e}")
        print("   (Other collectors will still work)")
        return True  # Don't fail pipeline


def run_job_matcher():
    """Step 4: Match jobs with resume using LLM"""
    print("\n" + "=" * 70)
    print("🤖 STEP 4: MATCHING JOBS WITH RESUME")
    print("=" * 70)

    try:
        result = subprocess.run(
            ["python", "job_matcher.py"],
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("❌ Job matching failed")
            return False

        print("\n✅ Job matching completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error running job matcher: {e}")
        return False


async def send_email():
    """Step 5: Send email with matched jobs"""
    print("\n" + "=" * 70)
    print("📧 STEP 5: SENDING EMAIL WITH JOB MATCHES")
    print("=" * 70)

    try:
        main_dir = Path(__file__).parent
        result = subprocess.run(
            ["python", "send_email_smtp.py"],
            cwd=main_dir,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("❌ Email sending failed")
            return False

        print("\n✅ Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


async def main():
    """Run complete pipeline"""
    print("\n" + "=" * 70)
    print("🎯 AUTOMATED JOB APPLICATION PIPELINE")
    print("=" * 70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nPipeline Steps:")
    print("1. 📊 Collect jobs from LinkedIn (real API)")
    print("2. 📚 Collect jobs from GitHub repositories")
    print("3. 🔥 Collect jobs from web sources (Firecrawl - optional)")
    print("4. 🤖 Match jobs with resume using LLM")
    print("5. 📧 Send top 50 matches via Gmail")
    print("=" * 70)

    # Step 1: Collect LinkedIn jobs
    linkedin_success = collect_linkedin_jobs()

    # Step 2: Collect GitHub jobs
    github_success = collect_github_jobs()

    # Step 3: Collect Firecrawl jobs (optional, won't fail pipeline)
    firecrawl_success = collect_firecrawl_jobs()

    # Check if we got any jobs from main sources
    if not linkedin_success and not github_success:
        print("\n❌ PIPELINE FAILED: No jobs collected from LinkedIn or GitHub")
        print("   (Firecrawl is optional and won't affect pipeline success)")
        sys.exit(1)

    # Step 3: Match jobs with resume
    if not run_job_matcher():
        print("\n❌ PIPELINE FAILED at job matching step")
        sys.exit(1)

    # Step 4: Send email
    if not await send_email():
        print("\n❌ PIPELINE FAILED at email sending step")
        sys.exit(1)

    # Success!
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📊 Summary:")
    print("  ✅ LinkedIn jobs collected")
    print("  ✅ GitHub jobs collected")
    if firecrawl_success:
        print("  ✅ Firecrawl jobs collected (web scraping)")
    else:
        print("  ⚠️  Firecrawl skipped (optional)")
    print("  ✅ Resume analyzed")
    print("  ✅ Jobs matched and ranked")
    print("  ✅ Top 50 matches identified")
    print("  ✅ Email sent with job details")
    print("\n📬 Check your inbox for job matches!")


if __name__ == "__main__":
    asyncio.run(main())
