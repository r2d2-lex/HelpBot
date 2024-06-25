import logging
from bs4 import BeautifulSoup
import asyncio
import sys
from crud import create_news
from db import get_db
sys.path.append("..")
from aiorequest import fetch_text
from schema.habr import HabrArt
from utils import get_date_time

HABR_NEWS_URL = 'https://habr.com/ru/hubs/python/articles/'
HABR_ROOT_URL = 'https://habr.com'


async def get_habr_news():
    return await fetch_text(HABR_NEWS_URL)

async def write_db(news):
    db = get_db()
    db_ = await db.__anext__()
    await create_news(db_, news)


async def main():
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
            await write_db(news)
        except AttributeError as err:
            logging.info(f'{err}')
            continue


if __name__ == '__main__':
    asyncio.run(main())
