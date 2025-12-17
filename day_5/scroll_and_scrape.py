import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scroll_and_scrape(url):
    """scrape a page by scrolling down it and gathering all quotes"""
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to the page
        await page.goto(url, wait_until='networkidle')
        
        # Scroll down to load all content
        previous_height = 0
        current_height = await page.evaluate('document.body.scrollHeight')
        
        while previous_height != current_height:
            # Scroll to bottom
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            
            # Wait for new content to load
            await page.wait_for_timeout(1000)  # Wait 1 second for content to load
            
            # Check if height changed
            previous_height = current_height
            current_height = await page.evaluate('document.body.scrollHeight')
        
        # Extract all quotes
        quotes = await page.evaluate('''() => {
            const quoteElements = document.querySelectorAll('div.quote');
            return Array.from(quoteElements).map(quote => {
                const text = quote.querySelector('span.text')?.textContent?.trim() || '';
                const author = quote.querySelector('small.author')?.textContent?.trim() || '';
                const tags = Array.from(quote.querySelectorAll('.tags .tag')).map(tag => tag.textContent?.trim()).filter(Boolean);
                return { text, author, tags };
            });
        }''')
        
        await browser.close()
        
        # Convert to DataFrame
        df = pd.DataFrame(quotes)
        return df

async def main():
    # Use the scroll version of quotes.toscrape.com
    url = "https://quotes.toscrape.com/scroll"
    df = await scroll_and_scrape(url)
    
    print(f"Found {len(df)} quotes")
    print("\nFirst few quotes:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = asyncio.run(main())