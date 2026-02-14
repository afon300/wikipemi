import os
import aiofiles
import aiohttp
import logging

class DataStorage:
    """
    Manages asynchronous storage of scraped data and static assets.
    """
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    async def save_page(self, title: str, content: str) -> bool:
        safe_filename = "".join(x for x in title if (x.isalnum() or x in "._- "))
        file_path = os.path.join(self.output_dir, f"{safe_filename}.html")
        
        try:
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Error saving {file_path}: {e}")
            return False

    async def download_assets(self, css_url: str, user_agent: str):
        """Downloads the base CSS to make local pages look like Wikipedia."""
        css_path = os.path.join(self.output_dir, "style.css")
        if os.path.exists(css_path):
            return

        self.logger.info("Downloading Wikipedia base CSS...")
        try:
            async with aiohttp.ClientSession(headers={'User-Agent': user_agent}) as session:
                async with session.get(css_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        async with aiofiles.open(css_path, "wb") as f:
                            await f.write(content)
                        self.logger.info("CSS saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to download CSS: {e}")
