from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
from urllib.parse import urlparse

class WebScraper:
    def __init__(self, headless=True):
        """Initialize the web scraper with options for headless browsing"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def search_website(self, url, search_term, search_selector=None):
        """
        Search a website for specific terms using its search functionality
        
        Parameters:
        - url: Website URL to search
        - search_term: Term to search for
        - search_selector: CSS selector for the search input field
        """
        try:
            self.driver.get(url)
            
            # Try common search input selectors if none provided
            search_selectors = [search_selector] if search_selector else [
                'input[type="search"]',
                'input[name="search"]',
                'input[name="q"]',
                '.search-input',
                '#search'
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if search_input:
                search_input.clear()
                search_input.send_keys(search_term)
                search_input.send_keys(Keys.RETURN)
                time.sleep(2)  # Wait for results to load
                return True
            return False
            
        except Exception as e:
            print(f"Error searching website: {e}")
            return False

    def extract_content(self, selectors):
        """
        Extract content from the current page using provided CSS selectors
        
        Parameters:
        - selectors: Dict of name:selector pairs to extract
        
        Returns:
        - Dict of extracted content
        """
        results = {}
        for name, selector in selectors.items():
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                results[name] = [elem.text for elem in elements]
            except NoSuchElementException:
                results[name] = []
        return results

    def scrape_multiple_pages(self, urls, selectors):
        """
        Scrape content from multiple pages
        
        Parameters:
        - urls: List of URLs to scrape
        - selectors: Dict of CSS selectors to extract from each page
        
        Returns:
        - DataFrame with extracted content
        """
        all_data = []
        
        for url in urls:
            try:
                self.driver.get(url)
                data = self.extract_content(selectors)
                data['url'] = url
                data['domain'] = urlparse(url).netloc
                all_data.append(data)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue
        
        return pd.DataFrame(all_data)

    def close(self):
        """Close the browser and clean up"""
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    # Initialize scraper
    scraper = WebScraper(headless=True)
    
    # Example 1: Search a website
    scraper.search_website(
        "https://example.com",
        "search term"
    )
    
    # Example 2: Scrape multiple pages
    urls = [
        "https://www.naukri.com/jobs-in-india",
        "https://in.linkedin.com/jobs/view/software-engineer-machine-learning-at-linkedin-4102540455?position=1&pageNum=0&refId=kmKv0UxNbvPnkycOVuhnzA%3D%3D&trackingId=dG06Z58K8hlk5miwELqaig%3D%3D",
    ]
    
    selectors = {
        'titles': 'h1',
        'paragraphs': 'p',
        'links': 'a'
    }
    
    results_df = scraper.scrape_multiple_pages(urls, selectors)
    results_df.to_csv('scraped_data.csv', index=False)
    
    # Clean up
    scraper.close()