from pipes import quote
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://quotes.toscrape.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Using the find_all method first as a recap but trying out the select method with css selectors instead
# quotes = soup.find_all('div', class_ = 'quote')

# Finding all the quotes containers using css selectors
quotes = soup.select('div.quote')

print(quotes)

print(f"Found {len(quotes)} quotes")


for quote in quotes:
    text = quote.select_one('span.text').text.strip()
    author = quote.select_one('small.author').text.strip()
    tags = quote.select_one('div.tags').text.strip()

    print(f"Quote: {text}")
    print(f"Author: {author}")
    print(f"Tags: {tags}")
    print("-" * 50)





######################################################## Pagination ########################################################


# More manual approach, sifting through each page based on the url
all_quotes = []

for page_num in range(1, 11):  # Pages 1-10
    url = f"https://quotes.toscrape.com/page/{page_num}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    quotes = soup.select('div.quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tags .tag')]

        all_quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })

# Convert to DataFrame
df = pd.DataFrame(all_quotes)

# Now you can do cool stuff:
print(df.head())           # First 5 rows
print(df.shape)            # (20, 3) - 20 books, 3 columns





# Using the "Next" button to navigate to the next page

all_quotes = []

url = "https://quotes.toscrape.com/page/1/"

while True:

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.select('div.quote')

    for quote in quotes:
        text = quote.find('span', class_='text').get_text(strip=True)
        author = quote.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tags .tag')]

        all_quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    next_btn = soup.select_one('li.next a')
    if next_btn:
        url = "https://quotes.toscrape.com" + next_btn['href']
    else:
        url = None

    if url is None:
        break

df = pd.DataFrame(all_quotes)

print(df.head(100))