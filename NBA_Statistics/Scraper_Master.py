#This script provides essential scraping functions that can be
#reused across multiple scrapers



from bs4 import BeautifulSoup as bs
import cloudscraper
import warnings

scraper = cloudscraper.create_scraper()

#Returns the beautifulsoup object for a given url
def Scrape_From_Source(url):

    page = None #set as empty, needs to have scope
    try:
        page = scraper.get(url)
    except:
        print("URL was invalid, please give valid URL")
        warnings.warn("Invalid URL: " + url)
        return -1
    
    soup = bs(page.content, 'html.parser')
    
    return soup