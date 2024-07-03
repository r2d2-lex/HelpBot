import logging
from bs4 import BeautifulSoup
import asyncio
import datetime
import sys
sys.path.append("..")
from db import get_db
from crawler.crud import create_news, read_news, get_one_news, delete_one_news

from aiorequest import fetch_text
from schema.habr import HabrArt
from utils import get_date_time

HABR_NEWS_URL = 'https://habr.com/ru/hubs/python/articles/'
HABR_ROOT_URL = 'https://habr.com'


async def get_habr_news():
    return await fetch_text(HABR_NEWS_URL)


def depends_db(func):
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


@depends_db
async def write_news_in_db(db_session, news):
    await create_news(db_session, news)


@depends_db
async def read_news_from_db(db_session, limit=15):
    return await read_news(db_session, limit)


@depends_db
async def delete_news_from_db(db_session, date):
    return await delete_one_news(db_session, date)


@depends_db
async def read_one_news_from_db(db_session, news_id):
    return await get_one_news(db_session, news_id)


async def parse_article(data)-> list:
    soup = BeautifulSoup(data, 'html.parser')
    articles = soup.findAll(class_='tm-articles-list__item')
    result = []

    for article in articles:
        try:
            # image_url = article.find(class_='tm-article-snippet__cover_cover tm-article-snippet__cover').find('img')['src']
            # image_content = await fetch_file(image_url)
            news = HabrArt(
                news_id = article['id'],
                title = article.find(class_='tm-title tm-title_h2').text,
                url = HABR_ROOT_URL + article.find(class_='tm-title__link')['href'],
                content =  article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2').find('p').text,
                published = get_date_time('%Y-%m-%d %H:%M:%S'),
                image_url = article.find(class_='tm-article-snippet__cover_cover tm-article-snippet__cover').find('img')['src']
                # image = image_content if image_content else bytes()
            )
            print_news(news)
            result.append(news)

        except AttributeError as err:
            logging.info(f'{err}')
            continue
    return result


async def news_update():
    with open('example.html', 'r') as file_descr:
        result = file_descr.read()
        news = await parse_article(result)
        for news_item in news:
            result = await read_one_news_from_db(news_item.news_id)
            if result:
                logging.info(f'News {news_item.news_id} already in db...')
                continue
            else:
                logging.info(f'News not in DB: {news_item.news_id}...')
                await write_news_in_db(news_item)


async def news_read():
    news = await read_news_from_db(15)
    for news_item in news:
        print_news(news_item)


async def delete_old_news():
    too_old = datetime.datetime.today() - datetime.timedelta(days=14)
    await delete_news_from_db(too_old)


async def main():
    # await news_update()
    await delete_old_news()


if __name__ == '__main__':
    asyncio.run(main())
