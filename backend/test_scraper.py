from scraper import run_scraper

def cb(msg, prog):
    print(f"[{prog}%] {msg}")

results = run_scraper("Plumbing in Hasilpur", cb)
print(f"Total found: {len(results)}")
has_web = [r for r in results if r.get("Has Website")]
no_web = [r for r in results if not r.get("Has Website")]
print(f"Has Website: {len(has_web)}")
print(f"No Website: {len(no_web)}")
