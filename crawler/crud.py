import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

import sys
sys.path.append("..")
from models.habr import News as ModelNews
from schema.habr import HabrArt as SchemaHabrArt


async def read_news(db:AsyncSession) -> list[SchemaHabrArt]:
    logging.info('Read news from db...')
    query = select(ModelNews)
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
