import sys
import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongo_utils import insert_job

# async def scrape_internshala_jobs():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)
#         page = await browser.new_page()
#         await page.goto("https://internshala.com/internships", timeout=60000)
#         await page.wait_for_selector(".individual_internship", timeout=15000)

#         print(" Scraping started...")

#         internships = await page.query_selector_all(".individual_internship")
#         print(f" Found {len(internships)} internships")

#         for internship in internships:
#             try:
#                 # Extract the correct job description page link
#                 link_tag = await internship.query_selector('a[href^="/internship/detail"]')
#                 if link_tag:
#                     job_href = await link_tag.get_attribute("href")
#                     job_link = f"https://internshala.com{job_href}" if job_href else "N/A"
#                 else:
#                     job_link = "N/A"

#                 job_data = {
#                     "link": job_link,
#                     "source": "Internshala",
#                     "scraped_at": datetime.utcnow()
#                 }

#                 insert_job(job_data)
#                 print(f" Saved: {job_link}")

#             except Exception as e:
#                 print(f" Error scraping internship: {e}")

#         await browser.close()


import pytz

async def scrape_internshala_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://internshala.com/internships", timeout=60000)
        await page.wait_for_selector(".individual_internship", timeout=15000)

        print(" Scraping..")

        internships = await page.query_selector_all(".individual_internship")
        print(f" Found {len(internships)} internships")

        for internship in internships:
            try:
                link_tag = await internship.query_selector('a[href^="/internship/detail"]')
                if link_tag:
                    job_href = await link_tag.get_attribute("href")
                    job_link = f"https://internshala.com{job_href}" if job_href else "N/A"
                    job_title = (await link_tag.inner_text()).strip() if job_href else "N/A"
                else:
                    job_link = "N/A"
                    job_title = "N/A"
                india_tz = pytz.timezone('Asia/Kolkata')
                job_data = {
                    "title": job_title,
                    "link": job_link,
                    "source": "Internshala",
                    "scraped_at": datetime.now(india_tz)
                }

                insert_job(job_data)
                print(f" Saved: {job_title} | {job_link}")

            except Exception as e:
                print(f" Error scraping internship: {e}")

        await browser.close()







#now we wil do for the linkedin jbobs

import sys
import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.mongo_utils import insert_job

USER_DATA_DIR = os.path.join(os.getcwd(), "jobright_user_data")

async def scrape_jobright_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False  
        )
        page = await browser.new_page()
        await page.goto("https://jobright.ai/", timeout=60000)
        if "login" in page.url or "signin" in page.url:
            print("please log in manually. You have 90 seconds...")
            await page.wait_for_timeout(90000)

        await page.goto("https://jobright.ai/jobs/recommend?pos=10", timeout=60000)
        print("found jobright recommended jobs")
        for _ in range(10):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight);")
            await page.wait_for_timeout(2000)
        jobs = await page.evaluate("""
            Array.from(document.querySelectorAll('a[href*="/jobs/"]')).map(a => ({
                link: a.href,
                title: a.textContent.trim()
            }))
        """)

        print(f"{len(jobs)} number of jobs available")

        india_tz = pytz.timezone('Asia/Kolkata')
        for job in jobs:
            job_data = {
                "title": job["title"],
                "link": job["link"],
                "source": "Jobright",
                "scraped_at": datetime.now(india_tz)
            }
            insert_job(job_data)
            print(f"saved: {job_data['title']} | {job_data['link']}")

        await browser.close()


#now we will do for glassdoor


import sys
import os
import asyncio
from datetime import datetime
import pytz
from playwright.async_api import async_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.mongo_utils import insert_job

USER_DATA_DIR = os.path.join(os.getcwd(), "glassdoor_user_data")

import pytz
from datetime import datetime
from playwright.async_api import async_playwright
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.mongo_utils import insert_job

USER_DATA_DIR = os.path.join(os.getcwd(), "glassdoor_user_data")

async def scrape_glassdoor_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False
        )
        page = await browser.new_page()
        await page.goto("https://www.glassdoor.co.in/Job/software-engineer-jobs-SRCH_KO0,17.htm", timeout=60000)
        if "login" in page.url or "signin" in page.url:
            print("🔐 Please log in to Glassdoor manually in the browser. You have 90 seconds...")
            await page.wait_for_timeout(90000)
            await page.goto("https://www.glassdoor.co.in/Job/software-engineer-jobs-SRCH_KO0,17.htm", timeout=60000)
        await page.wait_for_selector('a[data-test="job-link"]', timeout=20000, state="attached")
        for _ in range(10):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(2000)

        jobs = await page.evaluate("""
            Array.from(document.querySelectorAll('a[data-test="job-link"]')).map(a => {
                const labelledBy = a.getAttribute("aria-labelledby");
                let titleText = "Untitled";

                if (labelledBy) {
                    const titleId = labelledBy.split(' ')[0];
                    const titleEl = document.getElementById(titleId);
                    if (titleEl) {
                        titleText = titleEl.innerText.trim();
                    }
                }

                return {
                    link: a.href,
                    title: titleText
                };
            });
        """)

        print(f" {len(jobs)} jobs found on Glassdoor")

     
        india_tz = pytz.timezone('Asia/Kolkata')
        for job in jobs:
            job_data = {
                "title": job["title"],
                "link": job["link"],
                "source": "Glassdoor",
                "scraped_at": datetime.now(india_tz)
            }
            insert_job(job_data)
            print(f" Saved: {job_data['title']} | {job_data['link']}")

        await browser.close()




async def main():
    await scrape_glassdoor_jobs()
    await scrape_jobright_jobs()
    await scrape_internshala_jobs()
    #await scrape_jobright_jobs()

if __name__ == "__main__":
    asyncio.run(main())

    
# if __name__ == "__main__":
#     #asyncio.run(scrape_internshala_jobs())
#     asyncio.run(scrape_linkedin_jobs())
