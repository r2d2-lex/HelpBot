import datetime
import logging
from bs4 import BeautifulSoup
import asyncio
import sys
sys.path.append("..")
from aiorequest import fetch_text
from schema.habr import HabrArt

HABR_NEWS_URL = 'https://habr.com/ru/hubs/python/articles/'
HABR_ROOT_URL = 'https://habr.com'


def get_date_time(template):
    return datetime.datetime.now(tz=datetime.timezone.utc).strftime(template)


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
            news = HabrArt(
                news_id = article['id'],
                title = article.find(class_='tm-title tm-title_h2').text,
                url = HABR_ROOT_URL + article.find(class_='tm-title__link')['href'],
                content =  article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2').find('p').text,
                published = get_date_time('%Y-%m-%d %H:%M:%S'),
                image = bytearray()
            )
            print(f'{news.news_id}\r\n'
                  f'{news.title}\r\n'
                  f'{news.url}\r\n'
                  f'{news.content}\r\n'
                  f'{news.published}\r\n'
                  )
            print('\r\n')
        except AttributeError as err:
            logging.info(f'{err}')
            continue


if __name__ == '__main__':
    main()
