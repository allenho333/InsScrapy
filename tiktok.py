"""
This is an example web scraper for TikTok.com.

To run this scraper set env variable $SCRAPFLY_KEY with your scrapfly API key:
$ export $SCRAPFLY_KEY="your key from https://scrapfly.io/dashboard"
"""
import os
import json
import jmespath
from typing import Dict, List
from urllib.parse import urlencode, quote
from loguru import logger as log
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
from httpx import AsyncClient, Response
from parsel import Selector

# SCRAPFLY = ScrapflyClient(key=os.environ["SCRAPFLY_KEY"])

BASE_CONFIG = {
    # bypass tiktok.com web scraping blocking
    "asp": True,
    # set the proxy country to US
    "country": "AU",
}

# initialize an async httpx client
client = AsyncClient(
    # enable http2
    http2=True,
    # add basic browser like headers to prevent being blocked
    headers={
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
    },
)


def parse_post(response: ScrapeApiResponse) -> Dict:
    """parse hidden post data from HTML"""
    selector = response.selector
    data = selector.xpath("//script[@id='__UNIVERSAL_DATA_FOR_REHYDRATION__']/text()").get()
    post_data = json.loads(data)["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
    parsed_post_data = jmespath.search(
        """{
        id: id,
        desc: desc,
        createTime: createTime,
        video: video.{duration: duration, ratio: ratio, cover: cover, playAddr: playAddr, downloadAddr: downloadAddr, bitrate: bitrate},
        author: author.{id: id, uniqueId: uniqueId, nickname: nickname, avatarLarger: avatarLarger, signature: signature, verified: verified},
        stats: stats,
        locationCreated: locationCreated,
        diversificationLabels: diversificationLabels,
        suggestedWords: suggestedWords,
        contents: contents[].{textExtra: textExtra[].{hashtagName: hashtagName}}
        }""",
        post_data
    )
    return parsed_post_data

def parse_post_with_httpx(response: Response) -> Dict:
    """parse hidden post data from HTML"""
    assert response.status_code == 200, "request is blocked, use the ScrapFly codetabs"    
    selector = Selector(response.text)
    data = selector.xpath("//script[@id='__UNIVERSAL_DATA_FOR_REHYDRATION__']/text()").get()
    post_data = json.loads(data)["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
    parsed_post_data = jmespath.search(
        """{
        id: id,
        desc: desc,
        createTime: createTime,
        video: video.{duration: duration, ratio: ratio, cover: cover, playAddr: playAddr, downloadAddr: downloadAddr, bitrate: bitrate},
        author: author.{id: id, uniqueId: uniqueId, nickname: nickname, avatarLarger: avatarLarger, signature: signature, verified: verified},
        stats: stats,
        locationCreated: locationCreated,
        diversificationLabels: diversificationLabels,
        suggestedWords: suggestedWords,
        contents: contents[].{textExtra: textExtra[].{hashtagName: hashtagName}}
        }""",
        post_data
    )
    return parsed_post_data

async def scrape_posts(url: str) -> List[Dict]:
    """scrape tiktok posts data from their URLs"""
    to_scrape = [ScrapeConfig(url, **BASE_CONFIG) for url in urls]
    data = []
    async for response in SCRAPFLY.concurrent_scrape(to_scrape):
        post_data = parse_post_with_httpx(response)
        data.append(post_data)
    log.success(f"scraped {len(data)} posts from post pages")
    return data

async def scrape_post_with_httpx(url:str) -> Dict:
    """Scrape a single TikTok post's data from its URL."""
    try:
        # Make an HTTP GET request to the provided URL
        response = await client.get(url)

        # Parse the response and extract post data
        post_data = parse_post_with_httpx(response)

        log.success(f"Successfully scraped post from: {url}")
        return post_data
    except Exception as e:
        log.error(f"Failed to scrape post from {url}: {e}")
        return {}
