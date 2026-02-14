import asyncio
import aiohttp
import logging
from typing import Set, List
import time
import random

from wikipemi.config import ScraperConfig
from wikipemi.parser import WikiParser
from wikipemi.storage import DataStorage

class WikiScraper:
    """
    High-performance asynchronous Wikipedia scraper.
    """

    def __init__(self, config: ScraperConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.parser = WikiParser(config.base_url)
        self.storage = DataStorage(config.output_dir)
        
        self.url_stack: List[str] = []
        self.visited_urls: Set[str] = set()
        
        self.pages_scraped_count = 0
        self._count_lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(config.concurrency_limit)
        
        self.headers = {
            'User-Agent': config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    async def run(self):
        """Initializes assets and starts the crawl."""
        await self.storage.download_assets(self.config.css_url, self.config.user_agent)

        start_url = self.config.get_start_url()
        self.url_stack.append(start_url)
        
        self.logger.info(f"--- High-Speed Scraping Started ({self.config.concurrency_limit} concurrent workers) ---")
        self.logger.info(f"Initial URL: {start_url}")
        
        is_infinite = (self.config.max_pages <= 0)
        max_pages = self.config.max_pages if not is_infinite else float('inf')

        cookie_jar = aiohttp.CookieJar(unsafe=True)

        async with aiohttp.ClientSession(headers=self.headers, cookie_jar=cookie_jar) as session:
            tasks = set()
            
            while True:
                if self.pages_scraped_count >= max_pages:
                    break
                
                while len(tasks) < self.config.concurrency_limit and self.url_stack:
                    if self.pages_scraped_count + len(tasks) >= max_pages:
                        break
                        
                    url = self.url_stack.pop()
                    if url not in self.visited_urls:
                        task = asyncio.create_task(self._worker(session, url))
                        tasks.add(task)
                        task.add_done_callback(tasks.discard)

                if not tasks and not self.url_stack:
                    await asyncio.sleep(2)
                    if not tasks and not self.url_stack:
                        break
                
                if tasks:
                    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                else:
                    await asyncio.sleep(0.5)

        self.logger.info(f"--- Finished. Total Scraped: {self.pages_scraped_count} ---")

    async def _worker(self, session: aiohttp.ClientSession, url: str):
        async with self.semaphore:
            if url in self.visited_urls:
                return
            
            if self.config.request_delay > 0:
                await asyncio.sleep(self.config.request_delay + random.uniform(0.1, 0.5))
            
            try:
                async with session.get(url, timeout=self.config.request_timeout, allow_redirects=True) as response:
                    
                    if response.status == 403:
                        self.logger.error(f"403 Forbidden at {url}. (Bot blocked by firewall)")
                        return
                    
                    if response.status == 429:
                        self.logger.warning(f"429 Too Many Requests. Cooling down...")
                        await asyncio.sleep(5)
                        return

                    if response.status != 200:
                        self.logger.warning(f"Failed to fetch {url}: Status {response.status}")
                        return
                    
                    final_url = str(response.url)
                    self.visited_urls.add(final_url)
                    
                    html_text = await response.text()
                    
                    try:
                        clean_html, found_links, title = self.parser.parse(html_text)
                    except ValueError as ve:
                        self.logger.error(f"BLOCKED (Soft 200) on {url}: {ve}")
                        return
                    except Exception as parse_err:
                        self.logger.error(f"Parser error on {url}: {parse_err}")
                        return
                    
                    if not clean_html:
                        return

                    if await self.storage.save_page(title, clean_html):
                        async with self._count_lock:
                            self.pages_scraped_count += 1
                            if self.pages_scraped_count % 10 == 0 or self.pages_scraped_count < 10:
                                self.logger.info(f"Progress: {self.pages_scraped_count} pages saved.")

                    for link in found_links:
                        if link not in self.visited_urls:
                            self.url_stack.append(link)

            except Exception as e:
                self.logger.debug(f"Error scraping {url}: {e}")