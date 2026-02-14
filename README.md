# WikipEmi 🚀

**WikipEmi** is a professional-grade, high-performance Wikipedia text archiver. It is designed to download entire Wikipedia language editions while preserving structural integrity and providing a seamless local browsing experience.

## 🌟 Key Features

-   **High-Speed Asynchronous Core**: Built on `asyncio` and `aiohttp` for non-blocking network I/O, supporting high-concurrency downloads.
-   **Clean Structural Extraction**: Intelligent parsing that retains headers, paragraphs, lists, and tables while stripping images, videos, scripts, and UI junk.
-   **Local Style Injection**: Automatically downloads Wikipedia's "Vector" CSS and patches local HTML files for an authentic "offline" look.
-   **Internal Link Mapping**: Rewrites all internal Wikipedia links to point to your local `.html` files, enabling seamless offline navigation.
-   **Automatic Stack-based Crawling**: Starts from a random or specific page and follows internal links to build a comprehensive local knowledge base.
-   **Integrated Local Viewer**: Includes a dedicated web server script to browse your archive through a generated dashboard.

## 🛠️ Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/wikipemi.git
    cd wikipemi
    ```

2.  **Setup Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage Guide

### 1. Scrape Content
By default, the scraper will run indefinitely (`--max-pages -1`) and target French (`--lang fr`) or English.

```bash
# Scrape English Wikipedia with 15 workers
python main.py --lang en --concurrency 15 --output my_archive
```

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `--lang` | Wikipedia language code (en, fr, es, etc.) | `en` |
| `--output` | Directory for the local archive | `wiki_output` |
| `--concurrency` | Number of simultaneous connections | `10` |
| `--max-pages` | Limit downloads (-1 or 0 for infinite) | `-1` |
| `--start-url` | Specific Wikipedia URL to start from | `Random Page` |

### 2. View Local Archive
Browse your downloaded content using the integrated server:

```bash
python viewer.py --dir my_archive
```
Visit **`http://localhost:8000`** in your browser to explore your offline Wikipedia.

## 📂 Project Structure

-   `main.py`: CLI entry point.
-   `viewer.py`: Local dashboard and web server.
-   `wikipemi/`: Core package.
    -   `core.py`: Async task management & link stack logic.
    -   `parser.py`: HTML sanitization & structural extraction.
    -   `storage.py`: Async file I/O & asset management.
    -   `config.py`: Centralized browser-emulation & network settings.

## 🛡️ Bot Detection Avoidance
WikiPemi uses modern browser headers and automated "politeness" delays to minimize the risk of being flagged by Wikipedia's security systems. For massive scrapes, consider using a VPN or lower concurrency.

---
*Professional Archiving Made Simple.*
