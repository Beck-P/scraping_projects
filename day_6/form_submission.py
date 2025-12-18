import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def grab_html(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup



def extract_hidden_fields(soup):
    form_data = {}
    for input_tag in soup.find_all('input', type = 'hidden'):
        name = input_tag.get('name')
        value = input_tag.get('value')
        if name:
            form_data[name] = value
    
    return form_data


def get_form_action(soup, base_url):
    """Extract the form action URL"""
    form = soup.find('form')
    if form:
        action = form.get('action', '')
        # Handle relative URLs
        return urljoin(base_url, action)
    return base_url


def post_search(session, url, author_name, tag, form_data):
    form_data['author'] = author_name
    form_data['tag'] = tag
    form_data['submit_button'] = 'Search' 
    response = session.post(url, data = form_data)
    return response


def create_dataframe(soup):
    data = []
    quotes = soup.find_all('div', class_ = 'quote')
    for quote in quotes:
        content = quote.find('span',class_ ='content').text
        author = quote.find('span' ,class_ ='author').text
        tag = quote.find('span' ,class_ ='tag').text

        data.append({
            'content':content,
            'author':author,
            'tag':tag
        })
    df = pd.DataFrame(data)
    return df

def main():
    # Creating a session
    session = requests.Session()

    print("Starting Scraper...")
    # Set the url
    url = 'https://quotes.toscrape.com/search.aspx'

    # Grab the html from the site
    soup = grab_html(session, url)

    # Extract hidden fields and create form data
    form_data = extract_hidden_fields(soup)

    action_url = get_form_action(soup, url)

    # Submit the search with the term and updated form data
    author_name = 'Albert Einstein'
    tag = 'thinking'
    response = post_search(session, action_url, author_name, tag, form_data)
    
    # Parse the results
    search_soup = BeautifulSoup(response.text, 'html.parser')

    
    # Create a DataFrame with the results
    df = create_dataframe(search_soup)

    print(df)


if __name__ == "__main__":
    main()