import argparse
import logging
import asyncio
import sys
from wikipemi.core import WikiScraper
from wikipemi.config import ScraperConfig

def main():
    """
    Main entry point for the High-Performance WikiPemi application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="WikiPemi: Ultra-Fast Wikipedia Text & Structure Scraper"
    )
    
    parser.add_argument("--lang", type=str, default="en", help="Language code (default: en)")
    parser.add_argument("--output", type=str, default="wiki_output", help="Output folder")
    parser.add_argument("--start-url", type=str, help="Start URL")
    parser.add_argument("--max-pages", type=int, default=-1, help="Max pages (0 or -1 for infinite, default: -1)")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent workers (default: 10)")

    args = parser.parse_args()

    # Ensure lxml is available
    try:
        import lxml
    except ImportError:
        logger.error("The 'lxml' library is required for high-speed parsing.")
        logger.info("Please run: pip install lxml")
        sys.exit(1)

    config = ScraperConfig(
        language=args.lang,
        output_dir=args.output,
        start_url=args.start_url,
        max_pages=args.max_pages,
        concurrency_limit=args.concurrency
    )

    scraper = WikiScraper(config)
    
    try:
        asyncio.run(scraper.run())
    except KeyboardInterrupt:
        logger.info("Scraping stopped by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}")

if __name__ == "__main__":
    main()
