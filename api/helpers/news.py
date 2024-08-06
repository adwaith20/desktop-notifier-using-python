import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def scrape_news():
    url = 'https://www.bbc.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')

            news_articles = []

            # Find all news cards
            cards = soup.find_all('div', {'data-testid': 'dundee-card'})
            
            for card in cards:
                # Extract headline
                headline_elem = card.find('h2', {'data-testid': 'card-headline'})
                headline = headline_elem.text.strip() if headline_elem else 'No headline found'

                # Extract link
                link_elem = card.find('a', {'data-testid': 'internal-link'})
                link = 'https://www.bbc.com' + link_elem['href'] if link_elem else '#'


                news_articles.append({'title': headline, 'url': link, })

            return news_articles

        except aiohttp.ClientError as e:
            print(f"Error fetching data: {e}")
            return []


import requests

# Replace 'YOUR_API_KEY' with your actual News API key
NEWS_API_KEY = 'e874c404c2944e229abee1a7204fe7a3'
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'
PARAMS = {'country': 'in', 'apiKey': NEWS_API_KEY}

def fetch_news():
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=PARAMS)
        data = response.json()
        if data['status'] == 'ok':
            articles = data['articles']
            news_list = []
            for article in articles:
                title = article['title']
                description = article['description']
                url=article['url']
                date = article['publishedAt']
                news_list.append({'title': title, 'description': description,'url':url,'date':date})
            
            return news_list
        else:
            print(f"Error fetching news: {data['message']}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []

if __name__ == '__main__':
    fetched_news = fetch_news()
    print(fetched_news)
