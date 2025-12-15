import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"
response = requests.get(url)

## print("Status:", response.status_code)
## print("First 500 chars:")
## print(response.text[:500])
## print(response.content)
## print(response.headers)

soup = BeautifulSoup(response.text, 'html.parser')

# Find all book containers
books = soup.find_all('article', class_='product_pod')


book_list = []

for book in books:
    title = book.find('h3').a['title']
    price = book.find('p', class_='price_color').text
    in_stock = book.find('p', class_ = 'instock availability').text.strip()



    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"In Stock: {in_stock}")
    print("-" * 50)


    # Append each book as a dictionary
    book_list.append({
        'title': title,
        'price': price,
        'in_stock': in_stock
    })

# Convert to DataFrame
df = pd.DataFrame(book_list)

# Now you can do cool stuff:
print(df.head())           # First 5 rows
print(df.shape)            # (20, 3) - 20 books, 3 columns
print(df['price'])         # Just the prices