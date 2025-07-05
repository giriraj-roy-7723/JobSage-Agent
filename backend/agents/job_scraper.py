import sys
import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongo_utils import insert_job

async def scrape_internshala_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://internshala.com/internships", timeout=60000)
        await page.wait_for_selector(".individual_internship", timeout=15000)

        print("🔍 Scraping started...")

        internships = await page.query_selector_all(".individual_internship")
        print(f"✅ Found {len(internships)} internships")

        for internship in internships:
            try:
                # Extract the correct job description page link
                link_tag = await internship.query_selector('a[href^="/internship/detail"]')
                if link_tag:
                    job_href = await link_tag.get_attribute("href")
                    job_link = f"https://internshala.com{job_href}" if job_href else "N/A"
                else:
                    job_link = "N/A"

                job_data = {
                    "link": job_link,
                    "source": "Internshala",
                    "scraped_at": datetime.utcnow()
                }

                insert_job(job_data)
                print(f"🟢 Saved: {job_link}")

            except Exception as e:
                print(f"❌ Error scraping internship: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_internshala_jobs())
