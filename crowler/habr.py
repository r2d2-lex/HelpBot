from bs4 import BeautifulSoup
import asyncio
import sys
sys.path.append("..")
from aiorequest import fetch_text

HABR_NEWS_URL = 'https://habr.com/ru/hubs/python/articles/'

async def get_habr_news():
    return await fetch_text(HABR_NEWS_URL)

def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_habr_news())
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
