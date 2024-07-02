import logging
from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

import sys
sys.path.append("..")
from models.habr import News as ModelNews
from schema.habr import HabrArt as SchemaHabrArt


async def delete_one_news(db:AsyncSession, date: datetime):
    db_item = delete(ModelNews).where(ModelNews.published <= date)
    result = await db.execute(db_item)
    logging.info(f'Total rows deleted: {result.rowcount}')
    await db.commit()


async def get_one_news(db:AsyncSession, news_id: int) -> Union[ModelNews, None]:
    return await db.get(ModelNews, news_id)


async def read_news(db:AsyncSession, limit: int) -> list[SchemaHabrArt]:
    logging.info('Read news from db...')
    query = select(ModelNews).limit(limit).order_by(ModelNews.news_id.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_news(db: AsyncSession, item: SchemaHabrArt):
    logging.info('Create news record...')
    db_item = ModelNews(
        news_id = item.news_id,
        title = item.title,
        url = item.url,
        content = item.content,
        published = item.published,
        image_url = item.image_url,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
