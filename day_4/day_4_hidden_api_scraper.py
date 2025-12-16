import requests
import pandas as pd
import json

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://quotes.toscrape.com/scroll',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

page = 1

base_url = 'https://quotes.toscrape.com/api/quotes'

# response = requests.get(base_url, params={'page': page}, headers=headers)

all_data = []

while True:
    response = requests.get(base_url, params={'page': page}, headers=headers)
    data = response.json()
    all_data.extend(data['quotes'])
    # Stopping conditions (check ALL of these)
    if not data['has_next']:           # API says no more
        break
    if len(data) == 0:             # Empty response
        break
    if response.status_code != 200:    # Error occurred
        break
    
    print(f"Pulling in data from page: {page}")
    page += 1  # Move to next page

df = pd.DataFrame(all_data)



