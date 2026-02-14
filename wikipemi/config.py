from dataclasses import dataclass
from typing import Optional

@dataclass
class ScraperConfig:
    """
    Configuration settings for the Wikipedia Scraper.
    """
    language: str = "en"
    output_dir: str = "wiki_data"
    start_url: Optional[str] = None
    max_pages: int = -1 
    request_timeout: int = 20
    concurrency_limit: int = 2  # Keep it low for VPN stability
    request_delay: float = 1.0  # Politeness is key
    

    user_agent: str = "WikiPemiBot/1.0 (Educational; +https://github.com/wikipemi)"

    @property
    def base_url(self) -> str:
        return f"https://{self.language}.wikipedia.org"

    @property
    def css_url(self) -> str:
        return f"{self.base_url}/w/load.php?lang={self.language}&modules=skins.vector.styles.legacy&only=styles&skin=vector"

    def get_start_url(self) -> str:
        if self.start_url:
            return self.start_url
        return f"{self.base_url}/wiki/Special:Random"