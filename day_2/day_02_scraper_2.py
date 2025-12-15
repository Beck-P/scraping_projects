import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_page(url):
    """Scrape all quotes from a single page"""
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.select('div.quote')
    
    page_data = []
    for quote in quotes:
        # TODO: Extract text, author, tags
        # Hint: text = quote.select_one('span.text').text
        # Hint: tags = [tag.text for tag in quote.select('a.tag')]
        text = quote.select_one('span.text').text
        author = quote.select_one('small.author').text
        tags = [tag.text for tag in quote.select('a.tag')]

        page_data.append({
            'text':text,
            'author':author,
            'tags':tags
        })
    
    return page_data

def scrape_all_pages():
    """Scrape all pages using pagination"""
    all_quotes = []
    base_url = "https://quotes.toscrape.com"
    url = base_url + "/page/1/"
    page_num = 1
    
    while url:
        print(f"Scraping page {page_num}...")
        
        # Scrape current page
        quotes = scrape_page(url)
        all_quotes.extend(quotes)
        
        # Find next page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_btn = soup.select_one('li.next a')
        
        if next_btn:
            url = base_url + next_btn['href']
            page_num += 1
        else:
            url = None  # No more pages
    
    return all_quotes

# Main execution
if __name__ == "__main__":
    print("Starting scraper...")
    quotes = scrape_all_pages()
    
    # Save to CSV
    df = pd.DataFrame(quotes)
    df.to_csv('quotes.csv', index=False)
    print(f"✓ Saved {len(quotes)} quotes to quotes.csv")
    
    # Save to JSON
    with open('quotes.json', 'w') as f:
        json.dump(quotes, f, indent=2)
    print(f"✓ Saved {len(quotes)} quotes to quotes.json")