import requests
from bs4 import BeautifulSoup
import re
import time

class WebsiteScraper:
    def __init__(self, base_url):
        """Initialize the website scraper with the base URL of the company"""
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.scraped_data = {
            'about': '',
            'products': [],
            'contact': {},
            'social_media': {},
            'raw_text': []
        }

    def _get_soup(self, url):
        """Get BeautifulSoup object from URL"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_homepage(self):
        """Scrape the homepage for general information"""
        soup = self._get_soup(self.base_url)
        if not soup:
            return
        
        # Extract main content text
        main_content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for content in main_content:
            if content.text.strip():
                self.scraped_data['raw_text'].append(content.text.strip())
        
        # TODO: Extract more specific information

    def scrape_about_page(self):
        """Scrape the about page for company information"""
        about_urls = [
            f"{self.base_url}/about",
            f"{self.base_url}/about-us",
            f"{self.base_url}/company"
        ]
        
        for url in about_urls:
            soup = self._get_soup(url)
            if soup:
                about_content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                about_text = []
                for content in about_content:
                    if content.text.strip():
                        about_text.append(content.text.strip())
                
                if about_text:
                    self.scraped_data['about'] = ' '.join(about_text)
                    break

    def scrape_products(self):
        """Scrape product information"""
        product_urls = [
            f"{self.base_url}/products",
            f"{self.base_url}/collections",
            f"{self.base_url}/shop"
        ]
        
        for url in product_urls:
            soup = self._get_soup(url)
            if soup:
                # TODO: Extract product information
                # This is a placeholder for actual product extraction logic
                product_elements = soup.find_all('div', class_=re.compile(r'product|item'))
                for product in product_elements[:10]:  # Limit to first 10 for demonstration
                    product_name = product.find(['h2', 'h3', 'h4'])
                    product_price = product.find(string=re.compile(r'\$\d+'))
                    
                    if product_name:
                        self.scraped_data['products'].append({
                            'name': product_name.text.strip() if product_name else 'Unknown',
                            'price': product_price.strip() if product_price else 'Unknown'
                        })
                break

    def scrape_contact_info(self):
        """Scrape contact information"""
        contact_urls = [
            f"{self.base_url}/contact",
            f"{self.base_url}/contact-us"
        ]
        
        for url in contact_urls:
            soup = self._get_soup(url)
            if soup:
                # Look for email
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, str(soup))
                if emails:
                    self.scraped_data['contact']['email'] = emails[0]
                
                # Look for phone numbers
                phone_pattern = r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}'
                phones = re.findall(phone_pattern, str(soup))
                if phones:
                    self.scraped_data['contact']['phone'] = phones[0]
                
                # Look for address
                address_elements = soup.find_all(['address', 'p'], string=re.compile(r'street|avenue|boulevard|drive|road|lane', re.I))
                if address_elements:
                    self.scraped_data['contact']['address'] = address_elements[0].text.strip()
                
                break

    def scrape_social_media(self):
        """Extract social media links"""
        soup = self._get_soup(self.base_url)
        if not soup:
            return
        
        social_patterns = {
            'facebook': r'facebook\.com',
            'instagram': r'instagram\.com',
            'twitter': r'twitter\.com|x\.com',
            'linkedin': r'linkedin\.com',
            'pinterest': r'pinterest\.com',
            'tiktok': r'tiktok\.com'
        }
        
        for platform, pattern in social_patterns.items():
            links = soup.find_all('a', href=re.compile(pattern))
            if links:
                self.scraped_data['social_media'][platform] = links[0]['href']

    def scrape_all(self):
        """Run all scraping functions with delays to avoid rate limiting"""
        print(f"Scraping website: {self.base_url}")
        self.scrape_homepage()
        time.sleep(1)
        self.scrape_about_page()
        time.sleep(1)
        self.scrape_products()
        time.sleep(1)
        self.scrape_contact_info()
        time.sleep(1)
        self.scrape_social_media()
        
        return self.scraped_data

def scrape_website(url):
    """Main function to scrape a website and return structured data"""
    scraper = WebsiteScraper(url)
    return scraper.scrape_all()

if __name__ == "__main__":
    # Test the scraper
    test_url = "https://www.example.com"
    data = scrape_website(test_url)
    print(data) 