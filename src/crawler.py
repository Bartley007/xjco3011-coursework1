import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional

# DEBUG flag to control crawl delay
DEBUG = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuoteCrawler:
    """
    Crawler for https://quotes.toscrape.com/
    """
    BASE_URL = "https://quotes.toscrape.com"
    
    def __init__(self, delay: float = 6.0):
        self.delay = 0.1 if DEBUG else delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "QuoteSearchEngineCrawler/1.0"
        })

    def crawl_all_quotes(self) -> List[Dict[str, str]]:
        """
        Crawls all pages and extracts quotes, authors, and tags.
        """
        all_data = []
        current_page = "/page/1/"
        
        while current_page:
            url = f"{self.BASE_URL}{current_page}"
            logging.info(f"Crawling {url}...")
            
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                logging.error(f"Failed to crawl {url}: {e}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            
            for quote in quotes:
                text = quote.find('span', class_='text').get_text(strip=True)
                author = quote.find('small', class_='author').get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
                
                all_data.append({
                    "text": text,
                    "author": author,
                    "tags": ", ".join(tags),
                    "url": url
                })
            
            # Find next page link
            next_btn = soup.find('li', class_='next')
            current_page = next_btn.find('a')['href'] if next_btn else None
            
            if current_page:
                time.sleep(self.delay)
                
        return all_data

if __name__ == "__main__":
    crawler = QuoteCrawler()
    data = crawler.crawl_all_quotes()
    print(f"Crawled {len(data)} quotes.")
