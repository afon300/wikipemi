"""
WikiPemi: Professional Wikipedia Text & Structure Archiver
---------------------------------------------------------
Author: Interactive CLI Agent
License: MIT
"""

import re
from typing import List, Tuple
from bs4 import BeautifulSoup, Tag

class WikiParser:
    """
    Handles high-speed HTML parsing and structural extraction using lxml.
    Strips non-textual media while preserving logical document flow.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        # White-list of structural HTML tags to retain
        self.structure_tags = {
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 
            'table', 'tr', 'td', 'th', 'dl', 'dt', 'dd', 'blockquote'
        }

    def parse(self, html_content: str) -> Tuple[str, List[str], str]:
        """
        Extracts clean structure, internal links, and the page title.
        """
        soup = BeautifulSoup(html_content, 'lxml')

        # Extract and sanitize page title for file naming
        title_tag = soup.find('h1', id='firstHeading')
        title = title_tag.get_text().strip() if title_tag else "Unknown_Title"
        clean_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")

        # Target the main content container
        content_div = soup.find('div', id='bodyContent')
        if not content_div:
            return "", [], clean_title

        # Extract links before structural stripping
        links = self._extract_links(content_div)
        
        # Process the HTML to inject local styling and strip junk
        cleaned_html = self._clean_and_wrap(content_div, title)

        return cleaned_html, links, clean_title

    def _extract_links(self, soup_element: Tag) -> List[str]:
        """Identifies valid internal Wikipedia article links."""
        found_links = []
        for a_tag in soup_element.find_all('a', href=True):
            href = a_tag['href']
            # Filter for article namespace only (no colons, no anchors)
            if (href.startswith('/wiki/') and ':' not in href and '#' not in href):
                found_links.append(f"{self.base_url}{href}")
        return list(set(found_links))

    def _clean_and_wrap(self, soup_element: Tag, title: str) -> str:
        """
        Sanitizes the HTML tree and wraps it in a shell linked to local CSS.
        """
        # Remove non-structural and interactive elements
        for tag in soup_element.find_all(['script', 'style', 'img', 'video', 'audio', 'iframe', 'svg', 'noscript', 'form', 'input', 'button', 'link', 'meta']):
            tag.decompose()
        
        # Remove Wikipedia-specific UI clutter (edit links, navboxes, etc.)
        for tag in soup_element.find_all(class_=['mw-editsection', 'reference', 'noprint', 'mw-jump-link', 'catlinks', 'printfooter', 'ambox', 'navbox']):
            tag.decompose()

        # Final structural pass: localify links and strip formatting attributes
        for tag in soup_element.find_all(True):
            if tag.name == 'a' and tag.has_attr('href'):
                href = tag['href']
                if href.startswith('/wiki/') or href.startswith(self.base_url + '/wiki/'):
                    local_name = href.split('/')[-1]
                    tag['href'] = f"{local_name}.html"
            
            if tag.name not in self.structure_tags and tag.name != 'a':
                tag.unwrap()
            else:
                attrs = tag.attrs
                tag.attrs = {'href': attrs.get('href', '#'), 'class': 'local-link'} if tag.name == 'a' else {}

        # Construct the final standalone HTML document
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body {{ padding: 2rem; max-width: 900px; margin: auto; font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; color: #202122; }}
        .local-link {{ color: #36b; text-decoration: none; }}
        .local-link:hover {{ text-decoration: underline; }}
        h1 {{ border-bottom: 1px solid #a2a9f1; padding-bottom: 0.5rem; }}
    </style>
</head>
<body class="mediawiki">
    <div class="mw-body">
        <h1 class="firstHeading">{title}</h1>
        <div class="vector-body">{str(soup_element)}</div>
    </div>
</body>
</html>"""
