import logging
from bs4 import BeautifulSoup
import asyncio
import sys
from crud import create_news, read_news
from db import get_db
sys.path.append("..")
from aiorequest import fetch_text
from schema.habr import HabrArt
from utils import get_date_time

HABR_NEWS_URL = 'https://habr.com/ru/hubs/python/articles/'
HABR_ROOT_URL = 'https://habr.com'


async def get_habr_news():
    return await fetch_text(HABR_NEWS_URL)


def depends(func):
    async def wrapped(*args, **kwargs):
        db = get_db()
        db_ = await db.__anext__()
        return await func(db_, *args, **kwargs)
    return wrapped


def print_news(news: HabrArt):
    print(f'{news.news_id}\r\n'
          f'{news.title}\r\n'
          f'{news.url}\r\n'
          f'{news.content}\r\n'
          f'{news.published}\r\n'
          )


@depends
async def write_news_in_db(db_session, news):
    await create_news(db_session, news)


@depends
async def read_news_from_db(db_session):
    return await read_news(db_session)


async def parse_article(data)-> list:
    soup = BeautifulSoup(data, 'html.parser')
    articles = soup.findAll(class_='tm-articles-list__item')
    result = []

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
            print_news(news)
            result.append(news)

        except AttributeError as err:
            logging.info(f'{err}')
            continue
    return result


async def main():
    with open('example.html', 'r') as file_descr:
        result = file_descr.read()
        news = await parse_article(result)
        if news:
            for news_item in news:
                await write_news_in_db(news_item)

    # news = await read_news_from_db()
    # for news_item in news:
    #     print_news(news_item)


if __name__ == '__main__':
    asyncio.run(main())
