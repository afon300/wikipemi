import os
import time
import requests

import config
import nav
import extract

def download_css():
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        
    css_path = os.path.join(config.OUTPUT_DIR, "vector_style.css")
    if not os.path.exists(css_path):
        print(" Downloading the base CSS file...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(config.CSS_URL, headers=headers)
            response.raise_for_status()
            with open(css_path, 'wb') as f:
                f.write(response.content)
            print("CSS downloaded successfully.")
        except requests.RequestException as e:
            print(f" Error downloading CSS: {e}")
            
def crawler():
    download_css()
    
    urls_to_visit = [config.START_URL]
    visited_urls = set()
    pages_crawled = 0

    print("\n--- Starting crawl ---\n")
    while urls_to_visit and (pages_crawled < config.MAX_PAGES or config.MAX_PAGES == 0):
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue
        html_source, final_url = nav.go_to_page(current_url)
        if not html_source:
            continue
        visited_urls.add(current_url)
        visited_urls.add(final_url)
        pages_crawled += 1
    
        print(f"Processing page {pages_crawled}/{config.MAX_PAGES}...")
        print(f"Stack: {len(urls_to_visit)}")
    
        title = extract.extract_page_title(html_source)
        file_name = f"{title}.html"
        file_path = os.path.join(config.OUTPUT_DIR, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_source)
        print(f"Page saved: {file_name}")

        time.sleep(config.PAUSE_PER_PAGE)

        new_links = extract.extract_wikipedia_links(html_source)
        for link in new_links:
            if link not in visited_urls:
                urls_to_visit.append(link)
    
        print("-" * 20)

    print("--- Crawl finished ---")


if __name__ == "__main__":
    crawler()