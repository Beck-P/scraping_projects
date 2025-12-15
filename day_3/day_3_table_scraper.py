from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_stat_leaders_table(url):
    """Grab all of the data from the table in the url"""

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.select_one("#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child(61)")

    headers = [th.text.strip() for th in table.find_all('th')]

    rows = [tr.text for tr in table.find_all('tr')[1:]]

    cells = [td.text for td in table.find_all('td')]

    data = []

    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            data.append(dict(zip(headers, cells)))

    df = pd.DataFrame(data)
    
    return df


# Main Execution
if __name__ == "__main__":
    print("Getting scrapy...")

    url = 'https://en.wikipedia.org/wiki/2025%E2%80%9326_NBA_season'

    df = scrape_stat_leaders_table(url)

    print(df)

