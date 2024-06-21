from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.habr import News
import config
import logging

engine = create_engine(config.POSTGRES_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Database:
    def __init__(self):
        self.connection = None
        self.engine = create_engine(config.POSTGRES_DATABASE_URI)

    def __enter__(self):
        try:
            self.connection = self.engine.connect()
        except OperationalError:
            logging.error(f'database "{config.BOT_DB}" does not exist')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.connection.close()
            logging.info(f'Database "{config.BOT_DB}" connection closed!')

    def create_db(self):
        News.metadata.create_all(bind=self.engine)
        return

def create_tables():
    with Database() as db:
        db.create_db()

def main():
    create_tables()

if __name__ == '__main__':
    main()
