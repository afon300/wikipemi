import requests

def go_to_page(url):
    print(f"Navigating to: {url}")
    try:
        headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        final_url = response.url 
        print(f"Final URL: {final_url}")
        return response.text, final_url
    except requests.RequestException as e:
        print(f"error to {url}: {e}")
        return None, None