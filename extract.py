from bs4 import BeautifulSoup
from urllib.parse import urljoin
import config

def extract_wikipedia_links(html_source):
    found_links = []
    soup = BeautifulSoup(html_source, 'html.parser')
    base_url = f"https://{config.language}.wikipedia.org"

    for link in soup.find_all('a', href=True):
        href = link['href']

        if (href.startswith('/wiki/') and 
            ':' not in href and 
            '#' not in href):
            
            full_url = urljoin(base_url, href)
            found_links.append(full_url)
    unique_links = list(set(found_links))
    print(f"🔎 {len(unique_links)} unique links found on the page.")
    return unique_links

def extract_page_title(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    title_tag = soup.find('h1', id='firstHeading')
    if title_tag:
        return "".join(c for c in title_tag.text if c.isalnum() or c in (' ', '_')).rstrip()
    return "Unknown_Title"