from sqlalchemy import Column, DateTime, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'
    news_id = Column(Integer, unique=True, primary_key=True, index=True)
    title = Column(String)
    url = Column(String)
    content = Column(String)
    published = Column(DateTime)
    image_url = Column(String)
