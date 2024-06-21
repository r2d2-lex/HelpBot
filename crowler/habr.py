import logging
from bs4 import BeautifulSoup
import asyncio
import sys
sys.path.append("..")
from aiorequest import fetch_text

HABR_NEWS_URL = 'https://habr.com/ru/hubs/python/articles/'
HABR_ROOT_URL = 'https://habr.com'

async def get_habr_news():
    return await fetch_text(HABR_NEWS_URL)

def main():
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(get_habr_news())
    # loop.close()
    with open('example.html', 'r') as file_descr:
        result = file_descr.read()

    soup = BeautifulSoup(result, 'html.parser')
    articles = soup.findAll(class_='tm-articles-list__item')
    for article in articles:
        try:
            print(article['id'])
            print(article.find(class_='tm-title tm-title_h2').text)
            art_url = HABR_ROOT_URL + article.find(class_='tm-title__link')['href']
            print(art_url)
            print(article.find(class_='tm-article-snippet__cover_cover tm-article-snippet__cover').find('img')['src'])
            print(article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2').find('p').text)
            print('\r\n')
        except AttributeError as err:
            logging.info(f'{err}')
            continue


if __name__ == '__main__':
    main()
