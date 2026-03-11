#This script provides essential scraping functions that can be
#reused across multiple scrapers



from bs4 import BeautifulSoup as bs
import cloudscraper
import warnings
import time

_scraper = cloudscraper.create_scraper()

def reset_scraper():
    global _scraper
    _scraper = cloudscraper.create_scraper()

#Returns the beautifulsoup object for a given url
def Scrape_From_Source(url):

    page = None #set as empty, needs to have scope
    try:
        page = _scraper.get(url, timeout=30)
    except Exception as e:
        print(f"Request failed ({type(e).__name__}: {e}) — retrying with fresh session in 60s...")
        warnings.warn("Invalid URL: " + url)
        time.sleep(60)
        reset_scraper()
        try:
            page = _scraper.get(url, timeout=30)
        except Exception as e2:
            print(f"Retry also failed ({type(e2).__name__}: {e2})")
            return -1

    soup = bs(page.content, 'html.parser')

    return soup