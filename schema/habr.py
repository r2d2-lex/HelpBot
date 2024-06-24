from datetime import datetime

from pydantic import BaseModel


class HabrArt(BaseModel):
    news_id: int = 0
    title: str = ''
    url: str = ''
    content: str = ''
    published: datetime = None
    image: bytes = ''

    class Config:
        from_attributes = True
