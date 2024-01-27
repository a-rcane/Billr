from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from configs.config import settings


class DBOps:
    def __init__(self, connection_string=settings.DB_URI):
        self.connection_string = connection_string
        self.create = None

    def create_engine(self):
        if self.create is None:
            Base = declarative_base()
            engine = create_engine(settings.DB_URI, echo=True)
            self.create = Base.metadata.create_all(engine)
            return engine

    def create_session(self):
        if self.create_engine() is not None:
            Session = sessionmaker(bind=self.create_engine())
            return Session()


if __name__ == '__main__':
    db = DBOps()
