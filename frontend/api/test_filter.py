import asyncio
from scraper import run_scraper

async def main():
    print("Scraping 'Real Estate Agency in Dubai'...")
    def cb(msg, prog):
        pass
    results = await run_scraper("Real Estate Agency in Dubai", cb)
    print(f"Total scraped: {len(results)}")
    
    no_website = [r for r in results if not r.get("Has Website")]
    print(f"Total without website: {len(no_website)}")

asyncio.run(main())
