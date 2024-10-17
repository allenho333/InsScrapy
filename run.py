"""
This example run script shows how to run the Instagram.com scraper defined in ./instagram.py
It scrapes product data and product search and saves it to ./results/

To run this script set the env variable $SCRAPFLY_KEY with your scrapfly API key:
$ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
"""
from pathlib import Path
import asyncio
import json
import instagram
import tiktok

output = Path(__file__).parent / "results"
output.mkdir(exist_ok=True)


async def run():
    # enable scrapfly cache?
    instagram.BASE_CONFIG["cache"] = True
    instagram.BASE_CONFIG["debug"] = True
    tiktok.BASE_CONFIG["cache"] = True
    tiktok.BASE_CONFIG["debug"] = True
    print("running Instagram scrape and saving results to ./results directory")
    ins_post_content = await instagram.fallback_scrape_post("https://www.instagram.com/p/C_9l_-cTFJV/?igsh=N2Mwd3JyOWYzamFl")
    output.joinpath("food-multi-image-post-use-httpx-with-parse-post-function.json").write_text(json.dumps(ins_post_content, indent=2, ensure_ascii=False), encoding='utf-8')
    # print("running TikTok scrape and saving results to ./results directory")
    # tiktok_post_content = await tiktok.scrape_post_with_httpx("https://www.tiktok.com/@simple.home.edit/video/7309754078010051841?q=recipe%20blogger&t=1728859828193")
    # output.joinpath("oddanimalspecimens-video-post-use-httpx-with-parse-post-function.json").write_text(json.dumps(tiktok_post_content, indent=2, ensure_ascii=False), encoding='utf-8')




if __name__ == "__main__":
    asyncio.run(run())
